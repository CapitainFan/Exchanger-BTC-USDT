from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

button1 = KeyboardButton('/Получить_текущий_курс_BTC/USDT')
button2 = KeyboardButton('/Войти_в_аккаунт')
button3 = KeyboardButton('/Купить_пару_BTC/USDT')
button4 = KeyboardButton('/Продать_пару_BTC/USDT')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(button1).add(button2)