# from venv import create
import pymysql
from config import host, user, password, db_name
from config import bot, dp



def mysql_start():
    global db, cursor
    db = pymysql.connect(
        #host=host,
        port=3306,
        user=user,
        passwd=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    with db.cursor() as cursor:
        create_table_lessons = "CREATE TABLE IF NOT EXISTS lessons(img TEXT,\
        name VARCHAR(40),\
        description VARCHAR(255),\
        price  VARCHAR(40),\
        PRIMARY KEY(name))"
        cursor.execute(create_table_lessons)
        db.commit()
        create_table_records= "CREATE TABLE IF NOT EXISTS records(name VARCHAR(40),\
        client_name VARCHAR(100),\
        tel VARCHAR(40),\
        time VARCHAR(40))"
        cursor.execute(create_table_records)
        db.commit()
        print("table create")


async def mysql_add_lesson(state):
    async with state.proxy() as data:
        with db.cursor() as cursor:
            add_lesson = 'INSERT INTO lessons VALUES(%s, %s, %s, %s)'
            cursor.execute(add_lesson, tuple(data.values()))
            db.commit()

async def mysql_read(message):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM lessons")
        for lesson in cursor.fetchall():
            await bot.send_photo(message.from_user.id, lesson['img'], f'{lesson["name"]}\nОписание : {lesson["description"]}\nЦена {lesson["price"]}')


async def mysql_read2():
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM lessons')
        resultat = cursor.fetchall()
        return resultat



async def mysql_delete_command(data):
    with db.cursor() as cursor:
        cursor.execute('DELETE FROM lessons WHERE name = %s', (data,))
        db.commit()


async def mysql_enrollment_for_lesson(state):
    with db.cursor() as cursor:
        async with state.proxy() as data:
            cursor.execute('INSERT INTO records VALUES(%s, %s, %s, %s)', tuple(data.values()))
            db.commit()