import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
TEXT = '''Здравстуй дорогой пользователь!
Это телеграмм бот, который получает текущий курс BTC/USDT;
Позволяет продовать или покупать валютную пару 
BTC-WXG/USDT-WXG на криптоирже waves.exchange.
'''

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)