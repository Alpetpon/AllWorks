from aiogram import Router, F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, PhotoSize, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Union
import text, kb, config
import Database as db

router = Router()
# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage: MemoryStorage = MemoryStorage()

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

# Этот хэндлер будет срабатывать на "Создать резюме"
# и переводить бота в состояние ожидания ввода имени
@router.message(Text(text = text.create_resume))
async def fillname_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите ваше имя')
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
async def warning_not_name(message: Message):
    await message.answer(text='То, что вы отправили не похоже на имя\n\n'
                              'Пожалуйста, введите ваше имя\n\n'
                              'Если вы хотите прервать заполнение анкеты - '
                              'отправьте команду /cancel')

# Этот хэндлер будет срабатывать, если введен корректный возраст
# и переводить в состояние выбора пола

@router.message(StateFilter(Resume.age),
            lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
async def process_age_sent(message: Message, state: FSMContext):
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
async def warning_not_age(message: Message):
    await message.answer(
        text='Возраст должен быть целым числом от 4 до 120\n\n'
             'Попробуйте еще раз\n\nЕсли вы хотите прервать '
             'заполнение анкеты - отправьте команду /cancel')

# Этот хэндлер будет срабатывать на нажатие кнопки при
# выборе пола и переводить в состояние отправки фото
@router.callback_query(StateFilter(Resume.gender),
                   Text(text=['male', 'female', 'undefined_gender']))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
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
async def warning_not_gender(message: Message):
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
async def process_education_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные об образовании по ключу "education"
    await state.update_data(education=callback.data)


# Обработчик кнопки "Назад"
@router.message(lambda message: message.text == text.back)
async def Back_button(message: Message, state: FSMContext):
    curent_state = await state.get_state()
    if curent_state == Search.hub_choose_job:
        await state.set_state(Search.hub_create_resume)
        await message.answer("Вы вернулись к созданию резюме", reply_markup=kb.Main_keyboard)
    elif curent_state == Search.admin_panel:
        await  state.set_state(Search.start)
        await message.answer("Вы вернулись в начало", reply_markup=kb.start_keyboard)
    else:
        await message.answer("Нет такого состояния")

# Этот хэндлер будет срабатывать на отправку команды /showdata
# и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
@router.message(Text(text=text.show_resume), StateFilter(default_state))
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
        await message.answer(text='Вы еще не заполняли анкету. '
                                  'Чтобы приступить - отправьте '
                                  'команду /fillform')


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