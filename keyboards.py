from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



#Клавиатура клиента
b_lesson = KeyboardButton('Список занятий')
b_record = KeyboardButton('Записаться')
b_cancel_record = KeyboardButton("Отмена записи")
b_price = KeyboardButton("Цены")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b_lesson).add(b_record).add(b_cancel_record).add(b_price)

#Клавиатура админа
b_load_lesson = KeyboardButton('/Загрузить_урок')
b_delete_lesson = KeyboardButton('/Удалить_урок')
b_cancel = KeyboardButton("Отмена_загрузки")
b_load_price = KeyboardButton('/Загрузить_цену')
b_delete_price = KeyboardButton('/Удалить_цену')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.add(b_load_lesson).add(b_delete_lesson).add(b_cancel).add(b_load_price).add(b_delete_price)
