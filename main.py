import api
import keys
import tel
from keys import *
import numpy
import time
import threading
import sys, traceback
import logging
import requests
import asyncio
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Создаем переменную interval со значением "1m" или "1h"
interval = "1h"

# Создаем переменную seconds, которая содержит количество секунд в зависимости от значения переменной interval
if interval == "1h":
    seconds = 3600  # 1 час = 60 минут * 60 секунд
elif interval == "1m":
    seconds = 60  # 1 минута = 60 секунд

# def send_telegram_message(bot_token, chat_id, text):
#     """
#     Отправляет сообщение в телеграм бота.
#     :param bot_token: токен бота.
#     :param chat_id: идентификатор чата.
#     :param text: текст сообщения.
#     """
#     url = "https://api.telegram.org/bot%s/sendMessage" % keys.TELEGRAM_TOKEN
#     data = {
#         "chat_id": keys.TELEGRAM_CHAT_ID,
#         "text": text
#     }
#     response = requests.post(url, data=data)
#     if response.status_code != 200:
#         print("Ошибка отправки сообщения в телеграм:", response.text)
# def send_telegram_message(chat_id, text):
#     """
#     Отправляет сообщение в телеграм бота.
#     :param chat_id: идентификатор чата.
#     :param text: текст сообщения.
#     """
#     url = f"https://api.telegram.org/bot{keys.TELEGRAM_TOKEN}/sendMessage"
#     data = {
#         "chat_id": chat_id,
#         "text": text
#     }
#     response = requests.post(url, data=data)
#     if response.status_code != 200:
#         print("Ошибка отправки сообщения в телеграм:", response.text)
class SymbolThread(threading.Thread):
    def __init__(self, symbol):
        super(SymbolThread, self).__init__()
        self.symbol = symbol
        self.client = api.Binance_API(api_key=api_key, secret_key=secret_key)
        self.stop_event = threading.Event()
        self.wait_time = None

    def stop(self):
        self.stop_event.set()

    def run(self):
        # Ожидание начала новой минутной свечи
        self.wait_time = round(seconds - time.time() % seconds + 1)
        time.sleep(self.wait_time)
        while not self.stop_event.is_set():
            klines = self.client.get_candles(symbol=self.symbol, interval=interval)
            last_candle = klines[-1]
            if time.time() < last_candle[6]:
                klines.pop()

            numpy_klines = numpy.array(klines)
            close_price = numpy_klines[:, 4]
            close_price = close_price.astype(float)
            print("{} close_price: {}".format(self.symbol, close_price[-1]))
            message_text = (
                f"{self.symbol} close_price: {close_price[-1]}"
            )
            tel.send_telegram_message(keys.TELEGRAM_CHAT_ID, message_text)
            ema_short = api.ema(close_price, 2)
            ema_long = api.ema(close_price, 5)
            rsi = (api.rsi(close_price, 14))
            print("{} rsi: {}".format(self.symbol, rsi[-1]))
            message_text = (
                f"{self.symbol} rsi: {rsi[-1]}"
            )
            tel.send_telegram_message(keys.TELEGRAM_CHAT_ID, message_text)
            bol = (api.bollinger_breakout_strategy(close_price, 20, 2))
            positions, upper_band, lower_band = bol
            print("{} Positions: {}".format(self.symbol, positions[-1]))
            print("{} Upper Band: {}".format(self.symbol, upper_band[-1]))
            print("{} Lower Band: {}".format(self.symbol, lower_band[-1]))
            message_text = (
                f"{self.symbol} Positions: {positions[-1]}\n"
                f"{self.symbol} Upper Band: {upper_band[-1]}\n"
                f"{self.symbol} Lower Band: {lower_band[-1]}"
            )
            tel.send_telegram_message(keys.TELEGRAM_CHAT_ID, message_text)
            short_value = ema_short[-1]
            prev_short_value = ema_short[-2]
            long_value = ema_long[-1]
            prev_long_value = ema_long[-2]

            # Long
            if short_value > long_value and prev_short_value < prev_long_value and rsi[-1] > 70 and positions[-1] == 1:
                print("{} Long".format(self.symbol))
                qnt = 5  # значение количества, которое вы хотите использовать для торговли
                long = self.client.create_market_order(symbol=self.symbol, side='BUY', qnt=qnt)
                print("{} Bought {} units of {}".format(self.symbol, qnt, self.symbol.split("USDT")[0]))
                message_text = "{} купил {} единиц {}.".format(self.symbol, qnt, self.symbol.split("USDT")[0])
                tel.send_telegram_message(keys.TELEGRAM_CHAT_ID, message_text)

                # try:

                # except telegram.error.InvalidToken as e:
                #     logger.error("An error occurred: %s", e)
                    # here you can handle the InvalidToken error
                # except Exception as e:
                    # logger.error("An error occurred: %s", e, exc_info=True)
                    # here you can handle any other exceptions
                    # print(f'Ошибка при отправке уведомления: {e}')
                # В случае ошибки, код выполнится дальше, а не будет остановлен
            # Short
            elif prev_short_value > prev_long_value and short_value < long_value and rsi[-1] < 30 and positions[
                -1] == -1:
                print("{} Short".format(self.symbol))
                qnt = 5  # значение количества, которое вы хотите использовать для торговли
                short = self.client.create_market_order(symbol=self.symbol, side='SELL', qnt=qnt)
                print("{} Sold {} units of {}".format(self.symbol, qnt, self.symbol.split("USDT")[0]))

            else:
                print('{} No signal'.format(self.symbol))

            # Добавляем ожидание до следующей минутной свечи
            wait_time_next = round(seconds - time.time() % seconds + 1)
            print("До начала следующей минутной свечи: {} сек.".format(wait_time_next))
            time.sleep(wait_time_next)

        # Печатаем сообщение после того, как поток остановится
        print("Поток {} остановлен".format(self.symbol))


def start_threads():

    symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "XRPUSDT", "DOTUSDT", "BNBUSDT", "DOGEUSDT", "LTCUSDT", "LINKUSDT",
               "BCHUSDT"]
    threads = []

    # Запускаем отдельный поток для каждой криптовалютной пары
    for symbol in symbols:
        thread = SymbolThread(symbol)
        thread.start()
        threads.append(thread)
    wait_times = [thread.wait_time for thread in threads]
    print("До начала новой минутной свечи: {} сек.".format(min(wait_times)))
    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()

    # Печатаем сообщение после того, как все потоки завершили
    print("Все потоки завершены")


# async def run():
#     await tel.main()

if __name__ == '__main__':
    # tel.receive_telegram_message(keys.TELEGRAM_TOKEN)
    start_threads()
    # asyncio.run(run())
