import requests
from bs4 import BeautifulSoup

# Отправляем запрос с заголовками, чтобы избежать блокировки
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get("https://cbr.ru/currency_base/daily/", headers=headers)
response.raise_for_status()  # Проверяем успешность запроса

soup = BeautifulSoup(response.text, 'html.parser')

# Находим таблицу с курсами валют
table = soup.find('table', class_='data')

if table:
    # Получаем все строки таблицы (кроме заголовка)
    rows = table.find_all('tr')[1:]

    # Словарь для хранения курсов валют
    currency_rates = {}

    # Перебираем строки таблицы
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 5:  # Проверяем, что строка содержит все нужные столбцы
            currency_code = cols[1].text.strip()  # Код валюты (USD, EUR и т.д.)
            currency_name = cols[2].text.strip()  # Название валюты
            rate = cols[4].text.strip()  # Курс

            # Добавляем в словарь
            currency_rates[currency_code] = {
                'name':currency_name,
                'rate':rate
            }


    # Теперь можно получить конкретную валюту
    def get_currency_rate(currency_code):
        if currency_code in currency_rates:
            return currency_rates[currency_code]
        else:
            return None


    # Примеры использования
usd_rate = get_currency_rate('USD')
eur_rate = get_currency_rate('EUR')
cny_rate = get_currency_rate('CNY')

print("USD:", usd_rate)
print("EUR:", eur_rate)
print("CNY:", cny_rate)
