from aiogram import types, Dispatcher



async def no_command(message: types.Message):
    await message.answer("Нет такой команды")


def register_handlers_all(dp: Dispatcher):
    dp.register_message_handler(no_command)