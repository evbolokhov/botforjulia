# import telegram
# import asyncio
# import logging
#
# import keys
#
# logger = logging.getLogger(__name__)
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# handler = logging.StreamHandler()
# handler.setFormatter(formatter)
# logger.addHandler(handler)
#
#
# from telegram.error import NetworkError
# from  time import sleep
#
# # Замените <your_token> на токен вашего бота Telegram
# bot = telegram.Bot(token=keys.TELEGRAM_TOKEN)
#
# # chat_id - идентификатор чата в Telegram, куда будут отправляться уведомления
# # Замените <your_chat_id> на идентификатор вашего чата в Telegram
# chat_id = keys.TELEGRAM_CHAT_ID
#
#
# #def send_notification(text):
#     # offset = None
#     # while True:
#     # try:
#     #asyncio.run(_send_notification(text))
#     # except Exception as e:
#         # logger.error("An error occurred: %s", e, exc_info=True)
#
#
# # def send_notification(text):
# #     # Ожидайте завершения корутины Bot.send_message() с помощью await
# #
# #     while True:
# #         try:
# #             if text:
# #                 await bot.send_message(chat_id=chat_id, text=text)
# #             await asyncio.sleep(5)
# #
# #         except Exception as e:
# #             logger.error("An error occurred: %s", e, exc_info=True)
#
#
# # async def handle_messages():
# #     offset = None
# #     while True:
# #         try:
# #             updates = bot.get_updates(offset=offset, timeout=60)
# #             for update in updates:
# #                 message = update.message
# #                 if message:
# #                     # Обрабатывайте входящие сообщения здесь,
# #                     # например, отправляйте уведомления в другой чат
# #                     await bot.send_message(chat_id=chat_id, text=message.text)
# #                 offset = update.update_id + 1
# #         except telegram.TelegramError as error:
# #             # Обрабатывайте ошибки при получении обновлений здесь
# #             print(f'Error while receiving updates: {error}')
# #         await asyncio.sleep(1)
# #
# #
# # async def main():
# #     # Создайте задачу для корутины handle_messages(),
# #     # чтобы ее выполнение осуществлялось в отдельном потоке
# #     task = asyncio.create_task(handle_messages())
# #     await task
#
