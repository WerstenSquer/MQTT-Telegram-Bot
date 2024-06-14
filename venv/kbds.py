from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

start_kbd = ReplyKeyboardBuilder()
start_kbd.add(
    KeyboardButton(text='Добавить MAC-адрес'),
    KeyboardButton(text='Удалить MAC-адрес'),
    KeyboardButton(text='Просмотреть MAC-адреса'),
)

cancel_kbd = ReplyKeyboardBuilder()
cancel_kbd.add(
    KeyboardButton(text='Отмена')
)

