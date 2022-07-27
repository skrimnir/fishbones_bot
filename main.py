from aiogram import executor, types
from config import dp
from handlers import admin, client, all
from data_base import sqlite_db



async def on_startup(_):
    print("bot onlain")
    sqlite_db.sql_start()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
all.register_handlers_all(dp)

executor.start_polling(dp, skip_updates=True, on_startup = on_startup) # skip_updates скипает сообщения отправленные пока бот был не активен, функция on_startup выполняется только на старте


# 1 оформить заявку на пробное занятие
# 2 отправка заявки всем нужным людям (administrator)
# 3 save заявки в бд
# 4 выводит инфу о пробном занятии

