from aiogram import Router, F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.types import Message, CallbackQuery, PhotoSize, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Union
import text, kb, config
import Database as db

router = Router()


# Инициализируем Redis
redis: Redis = Redis(host='localhost')

storage: RedisStorage = RedisStorage(redis=redis)

# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, Union[str, int, bool]]] = {}


# Класс состояний бота
class Search(StatesGroup):
    start = State()  # Стартовая позиция
    hub_choose_spec = State()  # Выбор специальности
    hub_create_resume = State()  # Cоздание резюме
    hub_choose_job = State()  # Оценка вакансий
    create_resume = State()  # Создание резюме
    admin_panel = State() # Панель админа бота



# Класс состояний пользователя в резюме
class Resume(StatesGroup):
    start = State()
    name = State()
    surname = State()
    patronymic = State()
    age = State()
    gender = State()
    photo = State()
    education = State()
    wish_news = State()



# Обработчик команды /start
@router.message(Command(commands=["start"]))
async def Start_handler(message: Message, state: FSMContext):
    await db.cmd_start_db(message.from_user.id, message.from_user.username)
    if message.from_user.id == int(config.admin_alex_id):
        await message.answer("Вы авторизовались как администратор!", reply_markup= kb.admin_panel)
        await state.set_state(Search.admin_panel)
    else:
        await message.answer(text.greet.format(name=message.from_user.full_name),
                             reply_markup=kb.start_keyboard)


# Обработчик создания резюме или просмотра вакансий
@router.message(Text(text=text.start_search_job))
async def Main_hendler(message: Message, state: FSMContext):
    await state.set_state(Search.hub_create_resume)
    await state.set_state(Resume.start)
    await message.answer(text.resume, reply_markup=kb.Main_keyboard)


# Блок для создания резюме вручную

# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего. Вы вне машины состояний\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform')


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из машины состояний\n\n'
                              'Чтобы снова перейти к заполнению анкеты - '
                              'отправьте команду /fillform')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()

# Этот хэндлер будет срабатывать на команду /fillform
# и переводить бота в состояние ожидания ввода имени
@router.message(Text(text=text.create_resume_II))
async def Fillform_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите ваше имя', reply_markup=kb.Cancel_keyboard)
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(Resume.name)


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода возраста
@router.message(StateFilter(Resume.name), F.text.isalpha())
async def Name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите ваш возраст')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(Resume.age)


# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@router.message(StateFilter(Resume.name))
async def Not_name(message: Message):
    await message.answer(text='То, что вы отправили не похоже на имя\n\n'
                              'Пожалуйста, введите ваше имя\n\n'
                              'Если вы хотите прервать заполнение анкеты - '
                              'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если введен корректный возраст
# и переводить в состояние выбора пола
@router.message(StateFilter(Resume.age),
            lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
async def Age_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "age"
    await state.update_data(age=message.text)
    # Создаем объекты инлайн-кнопок
    male_button = InlineKeyboardButton(text='Мужской ♂',
                                       callback_data='male')
    female_button = InlineKeyboardButton(text='Женский ♀',
                                         callback_data='female')
    undefined_button = InlineKeyboardButton(text='🤷 Пока не ясно',
                                            callback_data='undefined_gender')
    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [[male_button, female_button],
                                                  [undefined_button]]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text='Спасибо!\n\nУкажите ваш пол',
                         reply_markup=markup)
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(Resume.gender)


# Этот хэндлер будет срабатывать, если во время ввода возраста
# будет введено что-то некорректное
@router.message(StateFilter(Resume.age))
async def Not_age(message: Message):
    await message.answer(
        text='Возраст должен быть целым числом от 4 до 120\n\n'
             'Попробуйте еще раз\n\nЕсли вы хотите прервать '
             'заполнение анкеты - отправьте команду /cancel')


# Этот хэндлер будет срабатывать на нажатие кнопки при
# выборе пола и переводить в состояние отправки фото
@router.callback_query(StateFilter(Resume.gender),
                   Text(text=['male', 'female', 'undefined_gender']))
async def Gender_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем пол (callback.data нажатой кнопки) в хранилище,
    # по ключу "gender"
    await state.update_data(gender=callback.data)
    # Удаляем сообщение с кнопками, потому что следующий этап - загрузка фото
    # чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    await callback.message.answer(text='Спасибо! А теперь загрузите, '
                                       'пожалуйста, ваше фото')
    # Устанавливаем состояние ожидания загрузки фото
    await state.set_state(Resume.photo)


# Этот хэндлер будет срабатывать, если во время выбора пола
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(Resume.gender))
async def Not_gender(message: Message):
    await message.answer(text='Пожалуйста, пользуйтесь кнопками '
                              'при выборе пола\n\nЕсли вы хотите прервать '
                              'заполнение анкеты - отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если отправлено фото
# и переводить в состояние выбора образования
@router.message(StateFilter(Resume.photo),
            F.photo[-1].as_('largest_photo'))
async def process_photo_sent(message: Message,
                             state: FSMContext,
                             largest_photo: PhotoSize):
    # Cохраняем данные фото (file_unique_id и file_id) в хранилище
    # по ключам "photo_unique_id" и "photo_id"
    await state.update_data(photo_unique_id=largest_photo.file_unique_id,
                            photo_id=largest_photo.file_id)
    # Создаем объекты инлайн-кнопок
    secondary_button = InlineKeyboardButton(text='Среднее',
                                            callback_data='secondary')
    higher_button = InlineKeyboardButton(text='Высшее',
                                         callback_data='higher')
    no_edu_button = InlineKeyboardButton(text='🤷 Нету',
                                         callback_data='no_edu')
    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [
                        [secondary_button, higher_button],
                        [no_edu_button]]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text='Спасибо!\n\nУкажите ваше образование',
                         reply_markup=markup)
    # Устанавливаем состояние ожидания выбора образования
    await state.set_state(Resume.education)


# Этот хэндлер будет срабатывать, если во время отправки фото
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(Resume.photo))
async def warning_not_photo(message: Message):
    await message.answer(text='Пожалуйста, на этом шаге отправьте '
                              'ваше фото\n\nЕсли вы хотите прервать '
                              'заполнение анкеты - отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если выбрано образование
# и переводить в состояние согласия получать новости
@router.callback_query(StateFilter(Resume.education),
                   Text(text=['secondary', 'higher', 'no_edu']))
async def Education_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные об образовании по ключу "education"
    await state.update_data(education=callback.data)
    # Создаем объекты инлайн-кнопок
    yes_news_button = InlineKeyboardButton(text='Да',
                                           callback_data='yes_news')
    no_news_button = InlineKeyboardButton(text='Нет, спасибо',
                                          callback_data='no_news')
    # Добавляем кнопки в клавиатуру в один ряд
    keyboard: list[list[InlineKeyboardButton]] = [
                                    [yes_news_button,
                                     no_news_button]]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Редактируем предыдущее сообщение с кнопками, отправляя
    # новый текст и новую клавиатуру
    await callback.message.edit_text(text='Спасибо!\n\n'
                                          'Остался последний шаг.\n'
                                          'Хотели бы вы получать новости?',
                                     reply_markup=markup)
    # Устанавливаем состояние ожидания выбора получать новости или нет
    await state.set_state(Resume.wish_news)


# Этот хэндлер будет срабатывать, если во время выбора образования
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(Resume.education))
async def warning_not_education(message: Message):
    await message.answer(text='Пожалуйста, пользуйтесь кнопками '
                              'при выборе образования\n\nЕсли вы хотите '
                              'прервать заполнение анкеты - отправьте '
                              'команду /cancel')


# Этот хэндлер будет срабатывать на выбор получать или
# не получать новости и выводить из машины состояний
@router.callback_query(StateFilter(Resume.wish_news),
                   Text(text=['yes_news', 'no_news']))
async def process_wish_news_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные о получении новостей по ключу "wish_news"
    await state.update_data(wish_news=callback.data == 'yes_news')
    # Добавляем в "базу данных" анкету пользователя
    # по ключу id пользователя
    user_dict[callback.from_user.id] = await state.get_data()
    # Завершаем машину состояний
    await state.clear()
    # Отправляем в чат сообщение о выходе из машины состояний
    await state.set_state(Search.hub_create_resume)
    await callback.message.edit_text(text='Спасибо! Ваши данные сохранены!\n\n')
    await callback.message.answer('Вы можеете перейти к просмотру вакансий', reply_markup=kb.Main_keyboard)


# Этот хэндлер будет срабатывать, если во время согласия на получение
# новостей будет введено/отправлено что-то некорректное
@router.message(StateFilter(Resume.wish_news))
async def warning_not_wish_news(message: Message):
    await message.answer(text='Пожалуйста, воспользуйтесь кнопками!\n\n'
                              'Если вы хотите прервать заполнение анкеты - '
                              'отправьте команду /cancel')


# Этот хэндлер будет срабатывать на отправку команды /showdata
# и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
@router.message(Text(text=text.show_resume))
async def process_showdata_command(message: Message):
    # Отправляем пользователю анкету, если она есть в "базе данных"
    if message.from_user.id in user_dict:
        await message.answer_photo(
            photo=user_dict[message.from_user.id]['photo_id'],
            caption=f'Имя: {user_dict[message.from_user.id]["name"]}\n'
                    f'Возраст: {user_dict[message.from_user.id]["age"]}\n'
                    f'Пол: {user_dict[message.from_user.id]["gender"]}\n'
                    f'Образование: {user_dict[message.from_user.id]["education"]}\n')
    else:
        # Если анкеты пользователя в базе нет - предлагаем заполнить
        await message.answer(text='Вы еще не заполняли анкету.')

@router.message(Text(text=text.check_job))
async def check_command(message: Message, state: FSMContext):
    await state.set_state(Search.hub_choose_job)
    await message.answer(text.test, reply_markup=kb.live_check_job)

# Обработчик кнопки "Назад"
@router.message(lambda message: message.text == text.back)
async def process_back_button(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == Search.hub_choose_job:
        await state.set_state(Search.hub_create_resume)
        await message.answer("Вы вернулись к созданию резюме.", reply_markup=kb.Main_keyboard)
    elif current_state == Search.admin_panel:
        await  state.set_state(Search.start)
        await message.answer("Вы вернулись в начало.", reply_markup=kb.start_keyboard)
    else:
        await message.answer("Нет такого состояния")

# Обработчик команды /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text.help.format(name=message.from_user.full_name))

@router.message(Command(commands = ['id']))
async def cmd_id(message: Message):
    await message.answer(f'Твой id:{message.from_user.id}')


# обработчик Админ-Панели
@router.message(Text(text = text.admin))
async def Admin_panel(message: Message):
    if message.from_user.id == int(config.admin_alex_id):
        await message.answer(text.admin_panel, reply_markup = kb.Main_panel)