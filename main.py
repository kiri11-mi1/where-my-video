import asyncio
import logging

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked, NetworkError, BotKicked

from app.config import TG_TOKEN, COMMANDS
from app.handlers import register_handlers, checking_updates, db


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot, loop=asyncio.get_event_loop())
register_handlers(dp)


async def scheduled(wait_for):
    while True:
        for chat in db.get_all_chats():
            updates = await checking_updates(chat.id)
            if updates:
                try:
                    await bot.send_message(chat.id, '\n'.join(updates), parse_mode='HTML')
                except (BotBlocked, BotKicked):
                    logging.error('Bot BLOCKED')
        await asyncio.sleep(wait_for)


if __name__ == '__main__':
    try:
        dp.loop.create_task(scheduled(60*60))
        executor.start_polling(dp, skip_updates=True)
    except NetworkError:
        logging.error('NETWORK ERROR')
