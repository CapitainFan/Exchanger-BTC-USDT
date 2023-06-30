import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()

TOKEN = os.getenv('TOKEN')
TEXT = '''Здравстуй дорогой пользователь!
Это телеграмм бот, который получает текущий курс BTC/USDT;
Позволяет продовать или покупать валютную пару 
BTC-WXG/USDT-WXG на криптоирже waves.exchange.
!!Бот работает только seed аккаунтами (без email)!!
'''

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)