from aiogram import types
from aiogram.dispatcher import Dispatcher
from app.config import START_MESSAGE, HELP_MESSAGE


async def start_command(message: types.Message):
    await message.answer(START_MESSAGE)


async def help_command(message: types.Message):
    await message.answer(HELP_MESSAGE)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
