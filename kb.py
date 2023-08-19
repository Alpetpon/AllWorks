from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import text

start_search_button: KeyboardButton = KeyboardButton(text=text.start_search_job)  # Кнопка для поиска работы без теста

# Клавиатура №1
start_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[start_search_button]],
                                                          resize_keyboard=True)  # Клавиатура которая встречает пользователя

Create_resume: KeyboardButton = KeyboardButton(text=text.create_resume)
Create_resume_II: KeyboardButton = KeyboardButton(text=text.create_resume_II)
Check_job: KeyboardButton = KeyboardButton(text=text.check_job)


# Клавиатура №2
Main_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[Create_resume], [Create_resume_II], [Check_job]],
                                                          resize_keyboard=True) # Клавиатура главного меню

like_button: KeyboardButton = KeyboardButton(text=text.like)
dislike_button: KeyboardButton = KeyboardButton(text=text.dis)
Chat_button: KeyboardButton = KeyboardButton(text=text.go_to_chat)
About_button: KeyboardButton = KeyboardButton(text=text.about)
Back_button: KeyboardButton = KeyboardButton(text=text.back)

# Клавиатура №3
live_check_job: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[like_button, dislike_button], [Chat_button, About_button], [Back_button]], resize_keyboard=True)# Клавиатура для просмотра анкет


admin_button: KeyboardButton = KeyboardButton(text = text.admin)
# Клавиатура №4
admin_panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[start_search_button], [admin_button]], resize_keyboard=True)


Stat_button:KeyboardButton = KeyboardButton(text = text.stat)
Block_button:KeyboardButton = KeyboardButton(text = text.block_text)
Unlock_button:KeyboardButton = KeyboardButton(text = text.unlock_text)

# Клавиатура №5
Main_panel:ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard = [[Stat_button], [Block_button], [Unlock_button], [Back_button]])




# Клавиатура пока не используется
spec_button: KeyboardButton = KeyboardButton(text=text.spis)
spec_button_1: KeyboardButton = KeyboardButton(text=text.spis)
search_button: KeyboardButton = KeyboardButton(text=text.search)



keyboard_job_1: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[spec_button], [spec_button_1], [search_button]],
                                                          resize_keyboard=True)# Клавиатура для выбора или поиска специальности