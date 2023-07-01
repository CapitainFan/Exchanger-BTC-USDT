import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from secret import TOKEN

TEXT = '''Бот запущен!
Для покупки или продажи BTC/USDT
войдите в ваш аккаунт waves.exchange
'''

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
