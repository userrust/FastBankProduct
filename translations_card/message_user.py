import requests


def send_message_user(chat_id, text):
    bot_token = "7520310595:AAFevgIKEx75UH3Z8tLnb5braLs66qUpflc"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"  # Используем переменную bot_token

    json = {
        "chat_id": chat_id,
        "text": text
    }

    headers = {"Accept":"application/json", "Content-Type":"application/json"}

    try:
        response = requests.post(url=url, headers=headers, json=json)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке сообщения: {e}")
        return None