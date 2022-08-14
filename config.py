from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv



load_dotenv()
storage = MemoryStorage()

host = os.getenv('host')
user = os.getenv("user")
password = os.getenv("password")
db_name = os.getenv("db_name")


BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

admin_id = [os.getenv('admin_id_antonm'), os.getenv('admin_id_vasyaz')]
administrator_id = [os.getenv('administrator_id_antonm')]
