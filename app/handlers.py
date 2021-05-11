from aiogram import types
from aiogram.dispatcher import Dispatcher


async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=['start'])
