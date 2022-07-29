from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



#Клавиатура клиента
b_lesson = KeyboardButton('Список занятий')
b_record = KeyboardButton('Записаться')
b_cancel_record = KeyboardButton("Отмена записи")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b_lesson).add(b_record).add(b_cancel_record)

#Клавиатура админа
b_load = KeyboardButton('/Загрузить')
b_delete = KeyboardButton('/Удалить')
b_cancel = KeyboardButton("Отмена_загрузки")

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.add(b_load).add(b_delete).add(b_cancel)
