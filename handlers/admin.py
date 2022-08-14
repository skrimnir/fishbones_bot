from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import admin_id, bot
from aiogram.dispatcher.filters import Text
from data_base import mysql_db
from keyboards import kb_admin
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



# создаём класс состояний
class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# вызвать клавиатуру администратора
async def send_to_admin(message: types.Message):
    if str(message.from_user.id) in admin_id:
        await bot.send_message(message.from_user.id, "Добро пожаловать, администратор", reply_markup=kb_admin)


# начало диолога для загрузки нового пункта меню
async def start_new_lesson(message: types.Message):
    if str(message.from_user.id) in admin_id:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')


# выход из состояния
async def cancel_hendler(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admin_id:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer("Отмена записи нового урока")


# ловим первый ответ и пишем в словварь
async def load_photo(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admin_id:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Введи название')


# ловим второй ответ
async def load_name(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admin_id:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи описание')


# ловим третий ответ
async def load_description(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admin_id:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Укажи цену')


# ловим последний ответ и используем полученные данные
async def load_price(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admin_id:
        async with state.proxy() as data:
            data['price'] = message.text

        # async with state.proxy() as data:
        #     await message.reply(str(data))
        await mysql_db.mysql_add_lesson(state)
        await state.finish()  # бот выходит из машины состояний и полностью удаляет всё введённую инфу. сохранять всё в бд нужно до жтой строчки!
        await message.answer("записан новый урок")


# запуск команды sql_delete_command и отправка админу сообщения о выполненном удалении
async def del_callback_run(callback_query: types.CallbackQuery):
    await mysql_db.mysql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удален.', show_alert=True)


# при нажатии на кнопку /Удалить вызывает уроки из дб и добавляет кнопку удалить под каждым
async def delete_lesson(message: types.Message):
    if str(message.from_user.id) in admin_id:
        read = await mysql_db.mysql_read2()
        for lesson in read:
            await bot.send_photo(message.from_user.id, lesson['img'], f'{lesson["name"]}\nОписание: {lesson["description"]}\nЦена {lesson["price"]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {lesson["name"]}', callback_data=f'del {lesson["name"]}')))


# Регистрируем хендлеры
def register_handlers_admin(dp: Dispatcher):
    # dp.register_message_handler(send_to_admin, state=)
    dp.register_message_handler(start_new_lesson, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_hendler, state="*", commands="cancel")
    dp.register_message_handler(cancel_hendler, Text(equals="Отмена_загрузки", ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(send_to_admin, commands='admin')
    dp.register_callback_query_handler(del_callback_run, Text(startswith="del "))  # если состояние начинается с 'del ', то запускается этот hendler
    dp.register_message_handler(delete_lesson, commands='Удалить')
