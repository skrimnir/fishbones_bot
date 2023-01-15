from os import stat
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import manager_id, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlalchemy
from keyboards import kb_manager
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



# вызвать клавиатуру манагера
async def send_to_manager(message: types.Message):
    if str(message.from_user.id) in manager_id:
        await bot.send_message(message.from_user.id, "Добро пожаловать, манагер", reply_markup=kb_manager)


# показть записи из бд
async def records_list(message: types.Message):
    await sqlalchemy.db_read_records(message)


def register_handlers_manager(dp: Dispatcher):
    dp.register_message_handler(send_to_manager, commands='manager')
    dp.register_message_handler(records_list, commands='Показать записи')
    dp.register_message_handler(records_list, Text(equals='Показать записи', ignore_case=True))