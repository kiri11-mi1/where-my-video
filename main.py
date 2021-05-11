import asyncio
import logging

from aiogram import Bot, types
from aiogram.types import BotCommand
from aiogram.dispatcher import Dispatcher

from app.config import TG_TOKEN
from app.handlers import register_handlers


logging.basicConfig(level=logging.INFO)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Начнём общение!'),
        BotCommand(command='/add', description='Добавлю YouTube канал.'),
        BotCommand(command='/del', description='Удалю YouTube канал.'),
        BotCommand(command='/check', description='Проверю, есть ли новые видео на каналах.'),
        BotCommand(command='/help', description='Дам подсказку, если забыл команды.'),
    ]

    await bot.set_my_commands(commands)


async def main():
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher(bot)
    

    register_handlers(dp)
    await set_commands(bot)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
