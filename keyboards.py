from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#Клавиатура клиента
b_lesson = KeyboardButton('/Список_занятий')
b_record = KeyboardButton('/Запсаться')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b_lesson)

#Клавиатура админа
b_load = KeyboardButton('/Загрузить')
b_delete = KeyboardButton('/Удалить')
b_cancel = KeyboardButton("Отмена_загрузки")

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.add(b_load).add(b_delete).add(b_cancel)
