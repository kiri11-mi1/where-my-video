import asyncio
import logging

from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from app.config import TG_TOKEN, COMMANDS
from app.handlers import register_handlers, checking_updates, db


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)


async def scheduled(bot, wait_for):
    while True:
        await asyncio.sleep(wait_for)

        for chat in db.get_all_chats():
            updates = await checking_updates(chat.id)
            if updates:
                await bot.send_message(chat.id, '\n'.join(updates), parse_mode='HTML')


async def main():
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher(bot, loop=asyncio.get_event_loop())
    register_handlers(dp)

    await bot.set_my_commands(COMMANDS)

    dp.loop.create_task(scheduled(bot, 60*60))

    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
