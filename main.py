from aiogram import executor
from config import BOT_TOKEN, dp
from handlers import admin, client, other
# from data_base import mysql_db
from data_base import sqlalchemy



async def on_startup(_):
    print("bot onlain")
    # mysql_db.mysql_start()
    sqlalchemy.start_db()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_all(dp)

executor.start_polling(dp, skip_updates=True, on_startup = on_startup) # skip_updates скипает сообщения отправленные пока бот был не активен, функция on_startup выполняется только на старте



# +  0) убрать токен из конфига и репозитория. Добавить локальный конфиг, в основном оставить None в конфиденциальных переменных
#    (номера админов можно тоже туда вынести)
# +  1) Перевести базу данных на MySQL, который разворачиваем в докер-контейнере
# +  2) Подключить ORM и написать модель - я обычно использую PonyORM или SQLAlchemy
# +  3) Добавить в БД таблицу с ценами и выводить цены в отдельном меню
# +  4) Поправить отправку заявки: оставить только выбор предмета. При отправке проверять открыт ли юзернейм в телеграме,
#    если нет, то спрашивать телефон (всегда спрашивать телефон)
# +  5) заявку записывать в БД: предмет, юзейрнейм, телефон (если есть в открытом доступе или юзер предоставил сам),
#    время и дата заявки
# +  6) отсылать заявку админинам в списке
# 7) добавить возможность просматривать заявки за определенный период для администраторов