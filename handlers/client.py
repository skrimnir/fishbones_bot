
from http import client
from posixpath import split
from time import time
from unicodedata import name
from aiogram import types, Dispatcher
from config import bot
from keyboards import kb_client
from data_base import mysql_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from config import administrator_id


# создаём класс состояний
class FSMAdmin(StatesGroup):
    name = State()
    client_name = State()
    tel = State()
    time = State()


# вызов клавиатуры клиента
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вас приветствует бот музыкальной школы fishbones', reply_markup=kb_client)


# показть список уроков из бд
async def occupations_list(message: types.Message):
    await mysql_db.mysql_read(message)


# начало диалога для записи на урок
async def enrollment_for_lesson(message: types.Message, state: FSMContext):
    read = await mysql_db.mysql_read2()
    for lesson in read:
                await bot.send_message(message.from_user.id, text=f'Записаться на урок: ', reply_markup=InlineKeyboardMarkup().\
                        add(InlineKeyboardButton(text=f'{lesson["name"]}', callback_data=f'rec {lesson["name"]}')))


# ответ на выбранный урок и запись названия урока
async def callback_rec(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMAdmin.name.set()
    await callback_query.message.answer(text=f'Вы хотите записаться на урок "{callback_query.data.replace("rec ", "")}"\nНапишите Ваше имя')
    async with state.proxy() as data:
        data['name'] = callback_query.data.replace("rec ", "")
    await callback_query.answer()
    await FSMAdmin.next()


# выход из состояния
async def cancel_record_hendler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Отмена записи на урок")


# ловим ответ, задаём вопрос
async def tell_your_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['client_name'] = message.text
    await FSMAdmin.next()
    await message.reply("Введите Ваш телефон")


# ловим ответ, задаём вопрос
async def tell_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tel'] = message.text
    await FSMAdmin.next()
    await message.reply('Напишите дату и время в виде ДД.ММ ЧЧ:ММ')



# финал записи на урок, отправка сообщения администратору, добавление данных в бд
async def finish_rec(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
    await mysql_db.mysql_enrollment_for_lesson(state)
    d = str(data)
    d = d.replace("FSMContextProxy state = 'FSMAdmin:time', data = {", "").replace("}, closed = True", "")
    for i in range(len(administrator_id)):
        await bot.send_message(administrator_id[i], text=f'Новая запись на урок: {d}')
    await state.finish()
    await message.answer("Вы записались")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(occupations_list, commands='Список_занятий')
    dp.register_message_handler(occupations_list, Text(equals='Список занятий', ignore_case=True))
    dp.register_message_handler(enrollment_for_lesson, commands='Записаться')
    dp.register_message_handler(enrollment_for_lesson, Text(equals='Записаться', ignore_case=True))
    dp.register_callback_query_handler(callback_rec, Text(startswith="rec "), state=None)
    dp.register_message_handler(cancel_record_hendler, state="*", commands="cancel")
    dp.register_message_handler(cancel_record_hendler, Text(equals="Отмена записи", ignore_case=True), state="*")
    dp.register_message_handler(tell_your_name, state=FSMAdmin.client_name)
    dp.register_message_handler(tell_time, state=FSMAdmin.tel)
    dp.register_message_handler(finish_rec, state=FSMAdmin.time)
