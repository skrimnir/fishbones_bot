from os import stat
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import admin_id, bot
from aiogram.dispatcher.filters import Text
# from data_base import mysql_db
from data_base import sqlalchemy
from keyboards import kb_admin
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



# создаём класс состояний для добавления урока
class FSMaddlesson(StatesGroup):
    photo = State()
    name = State()
    description = State()
    # price = State()


# создаём класс состаяний для цен
class FSMaddprice(StatesGroup):
    first_lesson_price = State()
    lesson_price = State()
    season_ticket = State()


# вызвать клавиатуру администратора
async def send_to_admin(message: types.Message):
    if str(message.from_user.id) in admin_id:
        await bot.send_message(message.from_user.id, "Добро пожаловать, администратор", reply_markup=kb_admin)


# начало диолога для загрузки нового урока
async def start_new_lesson(message: types.Message):
    if str(message.from_user.id) in admin_id:
        await FSMaddlesson.photo.set()
        await message.reply('Загрузи фото')


# выход из состояния
async def cancel_hendler(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admin_id:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer("Отмена записи")


# ловим первый ответ и пишем в словварь
async def load_photo(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admin_id:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMaddlesson.next()
        await message.reply('Введи название')


# ловим второй ответ
async def load_name(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admin_id:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMaddlesson.next()
        await message.reply('Введи описание')


# ловим третий ответ и используем полученные данные
async def load_description(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admin_id:
        async with state.proxy() as data:
            data['description'] = message.text
        # await FSMAdmin.next()
        # await message.reply('Укажи цену')
        await sqlalchemy.db_add_lesson(state)


# # ловим последний ответ и используем полученные данные
# async def load_price(message: types.Message, state: FSMContext):
#     if str(message.from_user.id) in admin_id:
#         async with state.proxy() as data:
#             data['price'] = message.text

#         # async with state.proxy() as data:
#         #     await message.reply(str(data))

#         await sqlalchemy.db_add_lesson(state)
        # await mysql_db.mysql_add_lesson(state)

        await state.finish()  # бот выходит из машины состояний и полностью удаляет всё введённую инфу. сохранять всё в бд нужно до этой строчки!
        await message.answer("записан новый урок")


# запуск команды db_delete_command_lesson и отправка админу сообщения о выполненном удалении
async def del_callback_run_lesson(callback_query: types.CallbackQuery):
    # await mysql_db.mysql_delete_command(callback_query.data.replace('del ', ''))
    await sqlalchemy.db_delete_command_lesson(callback_query.data.replace('del_lesson ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del_lesson ", "")} удален.', show_alert=True)


# при нажатии на кнопку /Удалить вызывает уроки из дб и добавляет кнопку удалить под каждым
async def delete_lesson(message: types.Message):
    if str(message.from_user.id) in admin_id:
        # read = await mysql_db.mysql_read2()
        read = await sqlalchemy.db_read_lessons_admin()
        for lesson in read:
            await bot.send_photo(message.from_user.id, lesson['img'], f'{lesson["name"]}\nОписание: {lesson["description"]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {lesson["name"]}', callback_data=f'del_lesson {lesson["name"]}')))


# начало диолога для загрузки цен
async def start_add_price(message: types.Message):
    if str(message.from_user.id) in admin_id:
        await FSMaddprice.first_lesson_price.set()
        await message.reply('Укажи цену первого урока и введи опиание')


# # выход из состояния
# async def cancel_hendler_price(message: types.Message, state: FSMContext):
#     if str(message.from_user.id) in admin_id:
#         current_state = await state.get_state()
#         if current_state is None:
#             return
#         await state.finish()
#         await message.answer("Отмена ввода цен")


# ловим первый ответ
async def load_first_lesson_price(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admin_id:
        async with state.proxy() as data:
            data['first_lesson_price'] = message.text
        await FSMaddprice.next()
        await message.reply('Укажите цену одного занятия и введите описание')


# ловим второй ответ и используем полученные данные
async def load_lesson_price(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admin_id:
        async with state.proxy() as data:
            data['lesson_price'] = message.text
        await FSMaddprice.next()
        await message.reply('Укажите цену абонимента и введите описание')



# ловим последний ответ и используем полученные данные
async def load_season_ticket_price(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admin_id:
        async with state.proxy() as data:
            data['season_ticket_price'] = message.text
        await sqlalchemy.db_add_price(state)
        await state.finish()  # бот выходит из машины состояний и полностью удаляет всё введённую инфу. сохранять всё в бд нужно до этой строчки!
        await message.answer("Информация добавленна")

# запуск команды db_delete_command_price и отправка админу сообщения о выполненном удалении
async def del_callback_run_price(callback_query: types.CallbackQuery):
    await sqlalchemy.db_delete_command_price(callback_query.data.replace('del_price ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del_price ", "")} удален.', show_alert=True)


# удаляем цену
async def delete_lesson_price(message: types.Message):
    if str(message.from_user.id) in admin_id:
        read = await sqlalchemy.db_read_price_admin()
        for price in read:
            await bot.send_message(message.from_user.id, text='----', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить_цену {price["lesson_price"]}', callback_data=f'del_price {price["lesson_price"]}')))



# Регистрируем хендлеры
def register_handlers_admin(dp: Dispatcher):
    # dp.register_message_handler(send_to_admin, state=)
    dp.register_message_handler(start_new_lesson, commands=['Загрузить_урок'], state=None)
    dp.register_message_handler(cancel_hendler, state="*", commands="cancel")
    dp.register_message_handler(cancel_hendler, Text(equals="Отмена_загрузки", ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMaddlesson.photo)
    dp.register_message_handler(load_name, state=FSMaddlesson.name)
    dp.register_message_handler(load_description, state=FSMaddlesson.description)
    # dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(send_to_admin, commands='admin')
    dp.register_callback_query_handler(del_callback_run_lesson, Text(startswith="del_lesson "))  # если состояние начинается с 'del_lesson ', то запускается этот hendler
    dp.register_message_handler(delete_lesson, commands='Удалить_урок')
    dp.register_message_handler(start_add_price, commands=['Загрузить_цену'], state=None)
    dp.register_message_handler(load_first_lesson_price, state=FSMaddprice.first_lesson_price)
    dp.register_message_handler(load_lesson_price, state=FSMaddprice.lesson_price)
    dp.register_message_handler(load_season_ticket_price, state=FSMaddprice.season_ticket)
    dp.register_callback_query_handler(del_callback_run_price, Text(startswith="del_price "))
    dp.register_message_handler(delete_lesson_price, commands='Удалить_цену')
