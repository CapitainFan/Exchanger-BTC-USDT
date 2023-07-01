import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()

TOKEN = os.getenv('TOKEN')
TEXT = '''Бот запущен!
Для покупки или продажи BTC/USDT
войдите в ваш аккаунт waves.exchange
'''

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
