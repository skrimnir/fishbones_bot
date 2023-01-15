from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, select, delete
from config import user, password, db_name
from config import bot, dp



# # метаданные - это информация о данных в бд
# meta = MetaData()

def start_db():
    global connect, lessons, records, meta, prices

    meta = MetaData()

    lessons = Table("lessons", meta,
        Column("img", String(500)),
        Column("name", String(40), primary_key=True),
        Column("description", String(255)),
        # Column("price", Integer)
    )

    records = Table("records", meta,
        Column("name", String(40)),
        Column("user_name", String(40)),
        Column("tel", String(40)),
        Column("time", String(40))
    )

    prices = Table("price", meta,
        Column("first_lesson_price", String (500)),
        Column("lesson_price", String(500)),
        Column("season_ticket_price", String(500)),
    )

    # подключаемся к бд
    engine = create_engine(f"mysql+pymysql://{user}:{password}@localhost/{db_name}")#, echo=True)
    meta.create_all(engine)
    print("podcluchil")
    connect = engine.connect()


async def db_add_lesson(state):
    async with state.proxy() as data:
        add_lesson = lessons.insert().values(img=data['photo'], name=data['name'] , description=data['description']) # , price=data['price']
        connect.execute(add_lesson)


async def db_read_lessons_client(message):
    show_lessons = lessons.select()
    result = connect.execute(show_lessons)
    for lesson in result:
        await bot.send_photo(message.from_user.id, lesson['img'], f'{lesson["name"]}\nОписание : {lesson["description"]}') # \nЦена {lesson["price"]}


async def db_read_lessons_admin():
    show_lessons = lessons.select()
    result = connect.execute(show_lessons)
    return result


async def db_delete_command_lesson(data):
    delete_lesson = lessons.delete().where(lessons.c.name == data)
    connect.execute(delete_lesson)


async def db_enrollment_for_lesson(state):
    async with state.proxy() as data:
        enrollment_for_lesson = records.insert().values(name=data["name"], user_name=data["user_name"], tel=data["tel"], time=data["time"]) # , client_name=data["client_name"]
        connect.execute(enrollment_for_lesson)


async def db_add_price(state):
    async with state.proxy() as data:
        add_price = prices.insert().values(first_lesson_price=data["first_lesson_price"], lesson_price=data["lesson_price"], season_ticket_price=data["season_ticket_price"])
        connect.execute(add_price)


async def db_read_price_admin():
    show_price = prices.select()
    result = connect.execute(show_price)
    return result


async def db_read_price_client(message):
    show_price = prices.select()
    result = connect.execute(show_price)
    for price in result:
        await bot.send_message(message.from_user.id, f'Пробный урок : {price["first_lesson_price"]}\nОдно занятие : {price["lesson_price"]}\nАбонимент : {price["season_ticket_price"]}')


async def db_delete_command_price(data):
    delete_price = prices.delete().where(prices.c.lesson_price == data)
    connect.execute(delete_price)


async def db_read_records(message):
    show_records = records.select()
    result = connect.execute(show_records)
    for record in result:
        await bot.send_message(message.from_user.id, f"урок : {record['name']}\nимя : {record['user_name']}\nтелефон : {record['tel']}\nвремя : {record['time']}")
# async def db_read_lessons_client(message):
#     show_lessons = lessons.select()
#     result = connect.execute(show_lessons)
#     for lesson in result:
        #  await bot.send_photo(message.from_user.id, lesson['img'], f'{lesson["name"]}\nОписание : {lesson["description"]}') # \nЦена {lesson["price"]}

#         Column("name", String(40)),
#         Column("user_name", String(40)),
#         Column("tel", String(40)),
#         Column("time", String(40))