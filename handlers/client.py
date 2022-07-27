from aiogram import types, Dispatcher
from config import bot
from keyboards import kb_client
from data_base import sqlite_db



#@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вас приветствует бот музыкальной школы fishbones', reply_markup=kb_client)


#@dp.message_handler(commands='Список_занятий')
async def occupations_list(message: types.Message):
    # await bot.send_message(message.from_user.id, 'Список в работе')
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(occupations_list, commands='Список_занятий')
