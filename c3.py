import requests
import json

# Замените значения переменных ниже своими собственными
api_key = 'Ваш_API_ключ'
api_secret = 'Ваш_API_секретный_ключ'
recipient_address = 'Адрес_получателя'
amount = 10  # Сумма для перевода

# Формирование запроса на перевод
data = {
    "sender": "Адрес_отправителя",
    "assetId": "WAVES",
    "recipient": recipient_address,
    "amount": amount,
    "fee": 100000,  # Комиссия в минимальных единицах (в данном случае 0.001 WAVES)
}

url = 'https://api.waves.exchange/v0/matcher/orderbook'
headers = {
    'Content-Type': 'application/json',
    'X-Api-Key': api_key,
    'X-Api-Secret': api_secret
}

# Отправка запроса на перевод
response = requests.post(url, headers=headers, data=json.dumps(data))

# Обработка ответа
if response.status_code == 200:
    print('Перевод выполнен успешно.')
else:
    print('Произошла ошибка при выполнении перевода.')
    print(response.text)
