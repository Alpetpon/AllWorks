from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import text

#Кнопка для начальной клавиатуры
start_search_button: KeyboardButton = KeyboardButton(text=text.start_search_job)
#Начальная клавиатура
start_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[start_search_button]],
                                                          resize_keyboard=True)


#Кнопки для клавиатура для просмотра вакансий
like_button: KeyboardButton = KeyboardButton(text=text.like)
dislike_button: KeyboardButton = KeyboardButton(text=text.dis)
Back_button: KeyboardButton = KeyboardButton(text=text.back)

#Клавиатура для просмотра вакансий
live_check_job: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[like_button, dislike_button], [Back_button]], resize_keyboard=True)

#Кдавиатура назад в машине состояний(Когда пользователь вводит свои данные)
Back:ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard = [[Back_button]])

#Кнопка для перехода в админ панель
admin_button: KeyboardButton = KeyboardButton(text = text.admin)
#Клавиатура для перехода в админ панель
admin_panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[start_search_button], [admin_button]], resize_keyboard=True)

#Кнопки для работы в админ панели
Stat_button:KeyboardButton = KeyboardButton(text = text.stat)
Block_button:KeyboardButton = KeyboardButton(text = text.block_text)
Unlock_button:KeyboardButton = KeyboardButton(text = text.unlock_text)

#Клавиатура для админ панели
Main_panel:ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[Stat_button], [Block_button], [Unlock_button], [Back_button]])

#Кнопка для перехода к просмотру вакансий
Check_vac: KeyboardButton = KeyboardButton(text = text.job)
#Клавиатура для перехода к просмотру вакансий
job_keyboard:ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard = [[Check_vac]])

