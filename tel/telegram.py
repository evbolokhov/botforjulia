import keys
import requests
import json


def send_telegram_message(chat_id, text):
    """
    Отправляет сообщение в телеграм бота.
    :param chat_id: идентификатор чата.
    :param text: текст сообщения.
    """
    url = f"https://api.telegram.org/bot{keys.TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("Ошибка отправки сообщения в телеграм:", response.text)


# def handle_message(message):
#     """
#     Обрабатывает сообщение от пользователя.
#     :param message: объект сообщения.
#     """
#     chat_id = message["chat"]["id"]
#     message_text = message["text"]
#
#     # Обработка команды "ping"
#     if message_text.lower() == "ping":
#         send_telegram_message(chat_id, "pong")
#
#
# def receive_telegram_message(bot_token):
#     """
#     Принимает сообщения от телеграм бота методом Webhook.
#     :param bot_token: токен бота.
#     """
#     url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
#     webhook_url = "https://your-webhook-url.com/webhook"
#     payload = {"url": webhook_url}
#     response = requests.post(url, json=payload)
#     if response.status_code == 200:
#         print("Webhook установлен.")
#     else:
#         print(f"Ошибка установки Webhook: {response.status_code} {response.text}")
#
#     # Обработка входящих сообщений
#     while True:
#         update = requests.get(f"https://api.telegram.org/bot{bot_token}/getUpdates?timeout=100")
#         if update.status_code == 200:
#             data = json.loads(update.content.decode('utf-8'))
#             if data["result"]:
#                 handle_message(data["result"][0]["message"])
#         else:
#             print(f"Ошибка получения обновлений: {update.status_code} {update.text}")