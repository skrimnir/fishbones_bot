from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

BOT_TOKEN = "5501225728:AAH6g1riVNnGBOaH31G6ByCe3XpE3UFTtE0"
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

admin_id = 304408643
administrator_id = 'pass'


