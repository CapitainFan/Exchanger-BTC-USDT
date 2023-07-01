import logging
from aiogram.utils import executor
from bot import dp
from handlers import client, admin, other
from background import keep_alive


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

client.register_handlers_client(dp)

keep_alive()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
