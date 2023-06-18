import telegram
from telegram.error import NetworkError
from  time import sleep

# Замените <your_token> на токен вашего бота Telegram
bot = telegram.Bot(token='<your_token>')

# chat_id - идентификатор чата в Telegram, куда будут отправляться уведомления
# Замените <your_chat_id> на идентификатор вашего чата в Telegram
chat_id = '<your_chat_id>'


def send_notification(text):
    import asyncio
    asyncio.run(_send_notification(text))


async def _send_notification(text):
    # Ожидайте завершения корутины Bot.send_message() с помощью await
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(f'Ошибка при отправке уведомления: {e}')




# import telegram
# from telegram.error import NetworkError, Unauthorized
#
# # Импортируем токен и chat_id из файла keys.py
# from keys import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
#
# class TelegramBot:
#     def __init__(self):
#         self.bot = telegram.Bot(token=TELEGRAM_TOKEN)
#
#     async def send_message(self, text):
#         try:
#             await self.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
#         except NetworkError:
#             print("Network Error occurred, trying again in 5 seconds...")
#             await asyncio.sleep(5)
#             await self.send_message(text)
#         except Unauthorized:
#             print("Unauthorized access, please check your token and chat ID.")
#
# async def main():
#     # Создаем объект класса TelegramBot
#     telegram_bot = TelegramBot()
#
#     # Отправляем сообщение
#     await telegram_bot.send_message("Hello, world!")
#
# # Запускаем корутину с помощью asyncio.run()
# if __name__ == "__main__":
#     asyncio.run(main())