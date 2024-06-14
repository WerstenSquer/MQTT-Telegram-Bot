from aiogram.types import BotCommand

private = [
    BotCommand(command='start', description='Начать'),
    BotCommand(command='add', description='Добавить MAC-адрес'),
    BotCommand(command='delete', description='Удалить MAC-адрес'),
    BotCommand(command='cancel', description='Отменить'),
    BotCommand(command='see_mac', description='Просмотреть MAC-адреса'),
]