import re
import logging

from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode

from app.messages import START_MESSAGE, HELP_MESSAGE, END_OF_QUOTA
from app.credentials import YT_TOKEN, DATABASE_URL
from app.db_api import DBApi
from app.yt_api import YTApi


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)

db = DBApi(DATABASE_URL)
yt = YTApi(YT_TOKEN)


async def start_command(message: types.Message):
    db.get_or_create_chat(message.chat.id)
    chat_name = message.chat.username or message.chat.title
    logging.info(f'{chat_name} START messaging')
    await message.answer(START_MESSAGE)


async def add_command(message: types.Message):
    chat = db.get_or_create_chat(message.chat.id)   
    chat_name = message.chat.username or message.chat.title
    channel_links = re.split('\s+', message.get_args())
    answers = ''
    for link in channel_links:
        if (chan_id := yt.get_channel_id_by_url(link)) == END_OF_QUOTA:
            return await message.answer(END_OF_QUOTA, ParseMode.HTML)
        elif chan_id:
            channel_name = yt.get_channel_name(chan_id)
            last_video_id = yt.get_last_video_id(chan_id)

            if not db.get_channel(id=chan_id, chat_id=chat.id):
                db.create_channel(
                    id=chan_id,
                    chat_id=chat.id,
                    last_video_id=last_video_id
                )
                answers += f'✅ Канал <a href=\'{link}\'>{channel_name}</a> успешно добавлен.\n'
                logging.info(f'{chat_name}: {channel_name} was ADDED')
            else:
                answers += f'⚠️ Канал <a href=\'{link}\'>{channel_name}</a> уже был добавлен.\n'
                logging.info(f'{chat_name}: {channel_name} ALREADY ADDED')
        else:
            answers += f'❌ Канал {link} не найден и не был добавлен...\n'
            logging.info(f'{chat_name}: Channel NOT FOUND')

    await message.answer(answers, ParseMode.HTML)


async def del_command(message: types.Message):
    chat = db.get_or_create_chat(message.chat.id)
    chat_name = message.chat.username or message.chat.title
    channel_links = re.split('\s+', message.get_args())
    answers = ''
    for link in channel_links:
        if (chan_id := yt.get_channel_id_by_url(link)) == END_OF_QUOTA:
            return await message.answer(END_OF_QUOTA, ParseMode.HTML)
        elif db.get_channel(id=chan_id, chat_id=chat.id):
            db.delete_channel(id=chan_id, chat_id=chat.id)
            channel_name = yt.get_channel_name(chan_id)
            answers += f'🗑 Удалил канал: <a href=\'{link}\'>{channel_name}</a>\n'
            logging.info(f'{chat_name}: {channel_name} was DELETED')
        else:
            answers += f'Не нашёл канал: {link}\n'
            logging.info(f'{chat_name}: Channel NOT FOUND')

    await message.answer(answers, ParseMode.HTML)


async def list_command(message: types.Message):
    chat = db.get_or_create_chat(message.chat.id)
    chat_name = message.chat.username or message.chat.title
    if not (channels := db.get_all_channels(chat.id)):
        return await message.answer(f'Нету каналов. Быстрей добавляй!')

    answers = ''
    for channel in channels:
        if (channel_name := yt.get_channel_name(channel.channel_id)) == END_OF_QUOTA:
            return await message.answer(END_OF_QUOTA, ParseMode.HTML)
        url = f'https://www.youtube.com/channel/{channel.channel_id}'
        channel_name = yt.get_channel_name(channel.channel_id)
        answers += f'🔷 <a href=\'{url}\'>{channel_name}</a>' + '\n'
        logging.info(f'{chat_name}: {channel_name}')

    await message.answer(answers, ParseMode.HTML)


async def help_command(message: types.Message):
    await message.answer(HELP_MESSAGE)


async def checking_updates(chat_id):
    chat = db.get_or_create_chat(chat_id)
    updates = []
    if not (channels := db.get_all_channels(chat.id)):
        updates.append(f'Нету каналов. Быстрей добавляй!')

    for channel in channels:
        if (current_last_video := yt.get_last_video_id(channel.channel_id)) == END_OF_QUOTA:
            return [END_OF_QUOTA]
        elif channel.last_video_id != current_last_video:
            channel.last_video_id = current_last_video
            db.session.commit()

            channel_url = f'https://www.youtube.com/channel/{channel.channel_id}'
            channel_name = yt.get_channel_name(channel.channel_id)

            video_url = f'https://www.youtube.com/watch?v={channel.last_video_id}'
            video_title = yt.video_title(channel.last_video_id)

            logging.info(f'{chat}: {channel_name} was UPDATED')

            updates.append(f'❗️ На канале <a href=\'{channel_url}\'>{channel_name}</a> вышло новое видео: <a href=\'{video_url}\'>{video_title}</a>')

    return updates


async def stat_command(message: types.Message):
    chat = db.get_or_create_chat(message.chat.id)
    chat_name = message.chat.username or message.chat.title
    logging.info(f'{chat_name}: STAT command')
    channels_count = len(db.get_all_channels(chat.id))
    await message.answer((
        '📈 Минутка статистики:\n\n'
        f'Количество каналов: <b>{channels_count}</b>'
    ), ParseMode.HTML)


async def check_command(message: types.Message):
    updates = await checking_updates(message.chat.id)
    if not updates:
        return await message.answer('Пока новых роликов нет!', ParseMode.HTML)
    await message.answer('\n'.join(updates), ParseMode.HTML)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(add_command, commands=['add'])
    dp.register_message_handler(list_command, commands=['list'])
    dp.register_message_handler(stat_command, commands=['stat'])
    dp.register_message_handler(check_command, commands=['check'])
    dp.register_message_handler(del_command, commands=['del'])
