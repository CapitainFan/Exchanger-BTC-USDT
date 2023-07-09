from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button1 = KeyboardButton('/Получить_текущий_курс_BTC/USDT')
button2 = KeyboardButton('/Вырбать_цену_для_покупки_пары_BTC/USDT')
button3 = KeyboardButton('/Выбрать_цену_для_продажи_пары_BTC/USDT')
button4 = KeyboardButton('/Подтвердить_платёж')


kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(button1).add(button2).add(button3).add(button4)