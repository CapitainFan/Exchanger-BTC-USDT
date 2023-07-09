import os
import asyncio
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN

TEXT = '''Бот запущен!
Для работы с криптовалютой бот использует биржу waves.exchange
'''

loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.MARKDOWN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)
