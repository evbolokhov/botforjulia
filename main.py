import api
from keys import *
import numpy
import time
import matplotlib.pyplot as plt

if __name__ == '__main__':
    client = api.Binance_API(api_key=api_key, secret_key=secret_key)

    while True:
        print(10 - time.time() % 10)
        time.sleep(10 - time.time() % 10 + 1)
        klines = client.get_candles(symbol="NEARUSDT", interval='1m')
        last_candle = klines[-1]
        # print(last_candle)
        # print(time.time(), last_candle[6])
        if time.time() < last_candle[6]:
            klines.pop()

        numpy_klines = numpy.array(klines)
        # print("numpy_klines", numpy_klines)
        close_price = numpy_klines[:, 4]
        close_price = close_price.astype(float)
        print("close_price:", close_price[-1])
        ema_short = api.ema(close_price, 2)
        ema_long = api.ema(close_price, 5)
        rsi = (api.rsi(close_price, 14))
        print("rsi:", rsi[-1])
        bol = (api.bollinger_breakout_strategy(close_price, 20, 2))
        positions, upper_band, lower_band = bol
        print("Positions:", positions[-1])
        print("Upper Band:", upper_band[-1])
        print("Lower Band:", lower_band[-1])
        # print(ema_short)
        short_value = ema_short[-1]
        prev_short_value = ema_short[-2]
        # print(short_value)
        # print(prev_short_value)
        # print(ema_long)
        long_value = ema_long[-1]
        prev_long_value = ema_long[-2]

        # Long
        if short_value > long_value and prev_short_value < prev_long_value and rsi[-1] > 70 and positions[-1] == 1:
            print("Long")
            long = client.create_market_order(symbol='NEARUSDT', side='BUY', qnt=3)
            print(long)
        # Short
        elif prev_short_value > prev_long_value and short_value < long_value and rsi[-1] < 30 and positions[-1] == -1:
            print("Short")
            short = client.create_market_order(symbol='NEARUSDT', side='SELL', qnt=3)
            print(short)
        else:
            print('No signal')
        # # генерируем данные
        # positions, upper_band, lower_band = api.bollinger_breakout_strategy(close_price, 20, 2)
        #
        # # рисуем график цен закрытия
        # plt.plot(close_price)
        #
        # # рисуем график верхней полосы Боллинджера
        # plt.plot(upper_band)
        #
        # # рисуем график нижней полосы Боллинджера
        # plt.plot(lower_band)
        #
        # # добавляем легенду
        # plt.legend(["Close Price", "Upper Band", "Lower Band"])
        #
        # # добавляем заголовок
        # plt.title("Bollinger Bands")
        #
        # # показываем график
        # plt.show()