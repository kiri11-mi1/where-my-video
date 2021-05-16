import asyncio
import logging

from aiogram import Bot, types, executor
from aiogram.types import BotCommand
from aiogram.dispatcher import Dispatcher

from app.config import TG_TOKEN, DATABASE_FILE
from app.handlers import register_handlers, checking_updates
from app.db_api import DBApi


logging.basicConfig(level=logging.INFO)


bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot, loop=asyncio.get_event_loop())
db = DBApi(DATABASE_FILE)

register_handlers(dp)


async def scheduled(wait_wor):
    while True:
        await asyncio.sleep(wait_wor)

        for chat in db.get_all_chats():
            updates = await checking_updates(chat.id)
            for update in updates:
                await bot.send_message(chat.id, update, parse_mode='HTML')


if __name__ == '__main__':
    dp.loop.create_task(scheduled(60*60*60))
    executor.start_polling(dp, skip_updates=True)
