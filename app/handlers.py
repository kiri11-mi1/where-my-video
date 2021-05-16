from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode

from app.config import START_MESSAGE, HELP_MESSAGE, YT_TOKEN, DATABASE_FILE
from app.db_api import DBApi
from app.yt_api import YTApi

import logging
import re


db = DBApi(DATABASE_FILE)
yt = YTApi(YT_TOKEN)


async def start_command(message: types.Message):
    db.get_or_create_chat(message.chat.id)
    await message.answer(START_MESSAGE)


async def add_command(message: types.Message):
    chat = db.get_or_create_chat(message.chat.id)
    channel_links = re.split('\s+', message.get_args())
    for link in channel_links:
        if chan_id := yt.get_channel_id_by_url(link):
            channel_name = yt.get_channel_name(chan_id)
            last_video_id = yt.get_last_video_id(chan_id)

            if not db.get_channel(id=chan_id, chat_id=chat.id):
                db.create_channel(
                    id=chan_id,
                    chat_id=chat.id,
                    last_video_id=last_video_id
                )
                answer = f'✅ Канал <a href=\'{link}\'>{channel_name}</a> успешно добавлен.'
                await message.answer(answer, ParseMode.HTML)
            else:
                answer = f'⚠️ Канал <a href=\'{link}\'>{channel_name}</a> уже был добавлен.'
                await message.answer(answer, ParseMode.HTML)
        else:
            await message.answer(f'❌ Канал {link} не найден и не был добавлен...')


async def del_command(message: types.Message):
    chat = db.get_or_create_chat(message.chat.id)
    channel_links = re.split('\s+', message.get_args())
    for link in channel_links:
        chan_id = yt.get_channel_id_by_url(link)
        if db.get_channel(id=chan_id, chat_id=chat.id):
            db.delete_channel(id=chan_id, chat_id=chat.id)
            channel_name = yt.get_channel_name(chan_id)
            answer = f'🗑 Удалил канал: <a href=\'{link}\'>{channel_name}</a>'
            await message.answer(answer, ParseMode.HTML)
        else:
            await message.answer(f'Не нашёл канал: {link}')


async def list_command(message: types.Message):
    chat = db.get_or_create_chat(message.chat.id)
    if not (channels := db.get_all_channels(chat.id)):
        await message.answer(f'Нету каналов. Быстрей добавляй!')

    for channel in channels:
        url = f'https://www.youtube.com/channel/{channel.channel_id}'
        channel_name = yt.get_channel_name(channel.channel_id)
        await message.answer(f'🔷 <a href=\'{url}\'>{channel_name}</a>', ParseMode.HTML)


async def help_command(message: types.Message):
    await message.answer(HELP_MESSAGE)


async def checking_updates(chat_id):
    chat = db.get_or_create_chat(chat_id)
    updates = ['Рассылка']
    if not (channels := db.get_all_channels(chat.id)):
        updates.append(f'Нету каналов. Быстрей добавляй!')

    for channel in channels:
        current_last_video = yt.get_last_video_id(channel.channel_id)
        if channel.last_video_id != current_last_video:
            channel.last_video_id = current_last_video

            channel_url = f'https://www.youtube.com/channel/{channel.channel_id}'
            channel_name = yt.get_channel_name(channel.channel_id)

            video_url = f'https://www.youtube.com/watch?v={channel.last_video_id}'
            video_title = yt.video_title(channel.last_video_id)

            updates.append(f'❗️ На канале <a href=\'{channel_url}\'>{channel_name}</a> вышло новое видео: <a href=\'{video_url}\'>{video_title}</a>')

    return updates


async def check_command(message: types.Message):
    updates = await checking_updates(message.chat.id)
    for update in updates:
        await message.answer(update, ParseMode.HTML)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(add_command, commands=['add'])
    dp.register_message_handler(list_command, commands=['list'])
    dp.register_message_handler(check_command, commands=['check'])
    dp.register_message_handler(del_command, commands=['del'])
