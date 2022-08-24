from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, select, delete
from config import user, password, db_name
from config import bot, dp



# # метаданные - это информация о данных в бд
# meta = MetaData()

def start_db():
    global connect, lessons, records, meta

    meta = MetaData()

    lessons = Table("lessons", meta,
        Column("img", String(500)),
        Column("name", String(40), primary_key=True),
        Column("description", String(255)),
        Column("price", Integer)
    )

    records = Table("records", meta,
        Column("name", String(40)),
        Column("client_name", String(100)),
        Column("tel", String(40)),
        Column("time", String(40))
    )
    # подключаемся к бд
    engine = create_engine(f"mysql+pymysql://{user}:{password}@localhost/{db_name}")#, echo=True)
    meta.create_all(engine)
    print("podcluchil")
    connect = engine.connect()


async def db_add_lesson(state):
    async with state.proxy() as data:
        add_lesson = lessons.insert().values(img=data['photo'], name=data['name'] , description=data['description'], price=data['price'])
        connect.execute(add_lesson)


async def db_read(message):
    show_lessons = lessons.select()
    result = connect.execute(show_lessons)
    for lesson in result:
        await bot.send_photo(message.from_user.id, lesson['img'], f'{lesson["name"]}\nОписание : {lesson["description"]}\nЦена {lesson["price"]}')


async def db_read2():
    show_lessons = lessons.select()
    result = connect.execute(show_lessons)
    return result


async def db_delete_command(data):
    delete_lesson = lessons.delete().where(lessons.c.name == data)
    connect.execute(delete_lesson)


async def db_enrollment_for_lesson(state):
    async with state.proxy() as data:
        enrollment_for_lesson = records.insert().values(name=data["name"], client_name=data["client_name"], tel=data["tel"], time=data["time"])
        connect.execute(enrollment_for_lesson)
    # with db.cursor() as cursor:
    #     async with state.proxy() as data:
    #         cursor.execute('INSERT INTO records VALUES(%s, %s, %s, %s)', tuple(data.values()))
    #         db.commit()
    #     add_lesson = lessons.insert().values(img=data['photo'], name=data['name'] , description=data['description'], price=data['price'])
    #         connect.execute(add_lesson)

# ins_lesson_name = lessons.insert().values(img="AgACAgIAAxkBAAIIY2L8AAH86-N5CYuZhPwFb4TrOcW_wgACfr8xGyxA4Us-cv-hUgo3hQEAAwIAA3MAAykE",name="gitara", description="ваще бомба!!!", price="100")
# conn.execute(ins_lesson_name)
# print("+ urok")