from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,ReplyKeyboardRemove)
import text

button_1: KeyboardButton = KeyboardButton(text=text.prof_false)#Кнопка для поиска работы без теста

#Клавиатура №1
keyboard_prof: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_1]],  resize_keyboard=True)#Клавиатура которая встречает пользователя


button_2: KeyboardButton = KeyboardButton(text = text.spis)
button_3: KeyboardButton = KeyboardButton(text = text.spis)
button_4: KeyboardButton = KeyboardButton(text = text.search)

keyboard_job_1: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_2], [button_3], [button_4]],  resize_keyboard=True)

button_12: KeyboardButton = KeyboardButton(text = text.create_resume)
button_13: KeyboardButton = KeyboardButton(text = text.create_resume_II)
button_14: KeyboardButton = KeyboardButton(text = text.check_job)
button_15: KeyboardButton = KeyboardButton(text = text.back)


keyboard_job_2: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_12, button_13], [button_15, button_14]], resize_keyboard=True)

button_16: KeyboardButton = KeyboardButton(text = text.like)
button_17: KeyboardButton = KeyboardButton(text = text.dis)
button_18: KeyboardButton = KeyboardButton(text = text.go_to_chat)
button_19: KeyboardButton = KeyboardButton(text = text.about)
button_20: KeyboardButton = KeyboardButton(text = text.back)


keyboard_job_3: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_16, button_17], [button_18, button_19], [button_20]], resize_keyboard=True)
