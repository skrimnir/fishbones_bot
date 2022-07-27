import sqlite3
from  config import bot
from aiogram import types, Dispatcher



def sql_start():
    global db, cursor
    db = sqlite3.connect('fishbones.db')
    cursor = db.cursor()
    if db:
        print('db connected ok')
    db.execute('CREATE TABLE IF NOT EXISTS lessons(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    db.commit()


async def sql_add_lesson(state):
    async with state.proxy() as data:
        cursor.execute('INSERT INTO lessons VALUES(?, ?, ?, ?)', tuple(data.values()))
        db.commit()


async def sql_read(message):
    for lesson in cursor.execute("SELECT * FROM lessons").fetchall():
        await bot.send_photo(message.from_user.id, lesson[0], f'{lesson[1]}\nОписание : {lesson[2]}\nЦена {lesson[3]}')


async def sql_read2():
    return cursor.execute('SELECT * FROM lessons').fetchall()


async def sql_delete_command(data):
    cursor.execute('DELETE FROM lessons WHERE name == ?', (data,))
    db.commit()