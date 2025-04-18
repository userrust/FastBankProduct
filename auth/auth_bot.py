import requests


def send_telegram_message(chat_id, code):
    bot_token = "7813157064:AAFxB7O2oxbxCNY8RTEgaVpdP0GH_H0b7Bs"  # Замените на токен вашего бота
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"  # Используем переменную bot_token

    payload = {
        "chat_id":chat_id,
        "text":f"Ваш код подтверждения: {code}"
    }

    headers = {"Accept":"application/json", "Content-Type":"application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Проверка на ошибки
        return response.json()  # Возвращает ответ от Telegram API
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке сообщения: {e}")
        return None
