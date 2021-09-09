from typing import Tuple
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

continue_button = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Продолжить'),
        KeyboardButton(text='Отмена')
    ]
],resize_keyboard=True, one_time_keyboard=True)

send_yet = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Отправить еще')
    ]
],resize_keyboard=True, one_time_keyboard=True)