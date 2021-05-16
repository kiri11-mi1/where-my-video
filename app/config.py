import os


TG_TOKEN = os.environ.get('TG_TOKEN')
YT_TOKEN = os.environ.get('YT_TOKEN')

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')

PORT = os.environ.get('PORT')
HOST = os.environ.get('HOST')


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