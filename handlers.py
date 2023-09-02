# Импортируем необходимые модули из библиотеки aiogram
from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram import types
from aiogram.types import Message

# Импортируем  модули необходимые для работы
import text, kb, config
import Database as db
#для работы api
import aiohttp

# Создаем экземпляр маршрутизатора
router = Router()

# Инициализируем Redis
redis: Redis = Redis(host='localhost')

# Инициализируем RedisStorage для Машины Конечных Состояний (FSM)
storage: RedisStorage = RedisStorage(redis=redis)


# Определяем группу состояний для бота
class Bot(StatesGroup):
    start = State()
    admin_panel = State()
    set_job = State()
    set_salary = State()
    set_town = State()


# Определяем группу состояний для резюме пользователя
class Resume(StatesGroup):
    start = State()
    job = State()
    salary = State()
    town = State()
    Check = State()


# Функция для проверки зарплаты
def is_valid_salary(text):
    try:
        salary = int(text)
        return salary >= 0
    except ValueError:
        return False


# Функция для проверки должности
def is_valid_job(text):
    # TODO добавить дополнительные проверки на корректность ввода
    return bool(text)


# Функция для проверки города
def is_valid_town(text):
    # TODO добавить дополнительные проверки на корректность ввода
    return bool(text)


# Обработчик для команды /start
@router.message(Command(commands=["start"]))
async def Start_handler(message: Message, state: FSMContext):
    # Вызываем функцию для обработки команды /start в базе данных
    await db.cmd_start_db(message.from_user.id, message.from_user.username)
    await state.set_state(Bot.start)
    if message.from_user.id == int(config.admin_alex_id):
        await message.answer("Вы авторизовались как администратор!", reply_markup=kb.admin_panel)
        await state.set_state(Bot.admin_panel)
    else:
        await message.answer(text.greet.format(name=message.from_user.full_name), reply_markup=kb.start_keyboard)


# Обработчик для текста "Начать поиск работы!"
@router.message(Text(text=text.start_search_job))
async def Fillform_command(message: Message, state: FSMContext):
    keyboard = types.ReplyKeyboardRemove()
    await message.answer(text='Пожалуйста введите желаемую должность ', reply_markup=keyboard)
    await state.set_state(Bot.set_job)
    await state.set_state(Resume.job)


# Обработчик для сообщений в состоянии Введите желаемую работу
@router.message(StateFilter(Resume.job))
async def job_sent(message: Message, state: FSMContext):
    job = message.text

    # Проверяем данные на "дурака"
    if not is_valid_job(job):
        await message.answer("Пожалуйста, введите корректную должность!")
        return

    await state.update_data(job=job)
    await message.answer(text='Спасибо!\n\nА теперь введите желаемую заработную плату:')
    await state.set_state(Bot.set_salary)
    await state.set_state(Resume.salary)


# Обработчик для сообщений в состоянии Ввода желаемой работы
@router.message(StateFilter(Resume.job))
async def salary_sent(message: Message, state: FSMContext):
    await state.update_data(job=message.text)
    await state.set_state(Bot.set_salary)
    await state.set_state(Resume.salary)


# Обработчик для сообщений в состоянии Введите желаемую зарплату
@router.message(StateFilter(Resume.salary))
async def salary_sent(message: Message, state: FSMContext):
    salary = message.text

    # Проверяем данные на "дурака"
    if not is_valid_salary(salary):
        await message.answer("Пожалуйста, введите корректную зарплату (положительное число)!")
        return

    await state.update_data(salary=salary)
    await message.answer(text='И последнее перед тем как найти вам работу, введите ваш город:')
    await state.set_state(Bot.set_town)
    await state.set_state(Resume.town)


# Обработчик для сообщений в состоянии Введите желаемую зарплату
@router.message(StateFilter(Resume.salary))
async def town_sent(message: Message, state: FSMContext):
    await state.update_data(salary=message.text)
    await state.set_state(Bot.set_town)
    await state.set_state(Resume.town)


# Обработчик для сообщений в состоянии Введите ваш город
@router.message(StateFilter(Resume.town))
async def town_sent(message: Message, state: FSMContext):
    town = message.text

    # Проверяем данные на "дурака"
    if not is_valid_town(town):
        await message.answer("Пожалуйста, введите корректный город!")
        return

    await state.update_data(town=town)
    await message.answer(text='Спасибо, теперь можно перейти в просмотр вакансий', reply_markup=kb.job_keyboard)


# Обработчик для сообщений в состоянии  Введите ваш город
@router.message(StateFilter(Resume.town))
async def close_test(message: Message, state: FSMContext):
    await state.update_data(town=message.text)
    await message.answer(text='Спасибо, теперь можно перейти в просмотру вакансий', reply_markup=kb.job_keyboard)



# Обработчик для кнопки перезапуска теста
@router.message(Text(text=text.re))
async def re_start(message: Message, state: FSMContext):
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("Вы начали процесс сбора данных заново.")
    await message.answer(text='Пожалуйста введите желаемую должность:',reply_markup=keyboard )
    await state.set_state(Resume.job)


async def search_hh_vacancies(job, salary, town):
    async with aiohttp.ClientSession() as session:
        url = f'https://api.hh.ru/vacancies'
        params = {
            'text': job,
            'salary': salary,
            'area': town,
        }
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('items', [])
            else:
                return None

@router.message(Text(text=text.job))
async def check_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()
    job = user_data.get('job', 'Не указано')
    salary = user_data.get('salary', 'Не указано')
    town = user_data.get('town', 'Не указано')
    vacancies = await search_hh_vacancies(job, salary, town)

    job = user_data.get('job', 'Не указано')
    salary = user_data.get('salary', 'Не указано')
    town = user_data.get('town', 'Не указано')
    print("Job:", job)  # Отладочное сообщение
    print("Salary:", salary)  # Отладочное сообщение
    print("Town:", town)  # Отладочное сообщение
    print("Vacancies:", vacancies)  # Отладочное сообщение

    if vacancies:
        await message.answer("Вот некоторые вакансии, которые соответствуют вашим критериям:")
        for vacancy in vacancies:
            title = vacancy.get('name', 'Не указано')
            employer = vacancy.get('employer', {}).get('name', 'Не указано')
            salary = vacancy.get('salary', {}).get('from', 'Не указано')
            await message.answer(f"Название: {title}\nРаботодатель: {employer}\nЗарплата от: {salary}")
    else:
        await message.answer("Извините, ничего не найдено по вашему запросу.")

    await state.clear()

# Обработчик для команды /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text.help.format(name=message.from_user.full_name))


# Обработчик для команды /id
@router.message(Command(commands=['id']))
async def cmd_id(message: Message):
    await message.answer(f'Твой id:{message.from_user.id}')


# Обработчик для текста "admin"
@router.message(Text(text=text.admin))
async def Admin_panel(message: Message):
    if message.from_user.id == int(config.admin_alex_id):
        await message.answer(text.admin_panel, reply_markup=kb.Main_panel)
