from aiogram import types
from aiogram.dispatcher import Dispatcher

from app.config import START_MESSAGE, HELP_MESSAGE, YT_TOKEN, DATABASE_FILE
from app.db_api import DBApi
from app.yt_api import YTApi

import logging


db = DBApi(DATABASE_FILE)
yt = YTApi(YT_TOKEN)


async def start_command(message: types.Message):
    db.get_or_create_chat(message.chat.id)
    await message.answer(START_MESSAGE)


async def add_command(message: types.Message):
    chat = db.get_or_create_chat(message.chat.id)
    channel_links = message.get_args().split(' ')
    for link in channel_links:
        if chan_id := yt.get_channel_id_by_name(link):
            last_video_id = yt.get_last_video_id(chan_id)

            if not db.get_channel(id=chan_id, chat_id=chat.id):
                channel = db.create_channel(
                    id=chan_id,
                    chat_id=chat.id,
                    last_video_id=last_video_id
                )
                message.answer(f'Канал {link} успешно добавлен')
            else:
                message.answer(f'Канал {link} уже был добавлен.')
        else:
            await message.answer(f'Канал {link} не добавлен')


async def del_command(message: types.Message):
    chat = db.get_or_create_chat(message.chat.id)
    channel_links = message.get_args().split(' ')
    for link in channel_links:
        pass


async def list_command(message: types.Message):
    chat = db.get_or_create_chat(message.chat.id)
    

async def help_command(message: types.Message):
    await message.answer(HELP_MESSAGE)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(add_command, commands=['add'])
    dp.register_message_handler(list_command, commands=['list'])

