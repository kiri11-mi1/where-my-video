from aiogram.types import BotCommand


COMMANDS = [
    BotCommand(command="/start", description="Давай начнём общение"),
    BotCommand(command="/help", description="Показывает список команд"),
    BotCommand(command="/check", description="Покажет новые ролики на каналах"),
    BotCommand(command="/list", description="При вызове этой команды, вы увидите список всех каналов"),
    BotCommand(command="/add", description="Добавит канал в чат"),
    BotCommand(command="/del", description="Удалит канал из чата"),
    BotCommand(command="/stat", description="Покажет статистику в чате"),
]


START_MESSAGE = (
    "Привет!\n"
    "Я бот, который будет присылать видосики с YouTube каналов, если меня об этом попросить!\n\n"
    "Кстати, насчёт просьб, чтобы я понимал, что я должен делать, используйте определённые команды.\n\n"
    "Тыкай /help, чтобы увидеть список."
)


HELP_MESSAGE = (
    '/add - Запомню любой YouTube канал и в дальнейшем буду присылать свежие ролики.\n\n'
    '/del - Удалю из своей памяти канал.\n\n'
    '/check - Вообще я сам проверяю новые видео на каналах, но если вы хотите проверить новинки самостоятельно, то используйте эту команду.\n\n'
    '/list - Покажу тебе список всех каналов, которые ты добавил.'
)

END_OF_QUOTA = '😭 Я совсем устал!\nОклемаюсь и опять начну работать.'