from aiogram import types
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,ReplyKeyboardRemove)
import text

# Создаем объекты кнопок
button_1: KeyboardButton = KeyboardButton(text=text.prof_true)
button_2: KeyboardButton = KeyboardButton(text=text.prof_false)

# Создаем объект клавиатуры, добавляя в него кнопки
keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_1, button_2]],
                                                    resize_keyboard=True,
                                                    input_field_placeholder=text.Press_button
                                                    )

