# Импортируем необходимые модули из библиотеки aiogram
from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram import types
from aiogram.types import Message

# Импортируем модули необходимые для работы
import text, kb, config
import Database as db
# для работы api
import aiohttp

# Создаем экземпляр маршрутизатора
router = Router()

# Инициализируем Redis
redis: Redis = Redis(host='localhost')

# Инициализируем RedisStorage для Машины Конечных Состояний (FSM)
storage: RedisStorage = RedisStorage(redis=redis)

# Ваш словарь для хранения данных пользователей
user_data_dict = {}


# Определяем группу состояний для бота
# Определяем группу состояний для бота
class Bot(StatesGroup):
    start = State()
    admin_panel = State()
    like = State()
    dislike = State()



# Определяем группу состояний для резюме пользователя
class Resume(StatesGroup):
    start = State()
    job = State()
    salary = State()
    country = State()
    town = State()
    Choise = State()
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


# Функция для проверки страны
def is_valid_country(text):
    # TODO: Добавьте дополнительные проверки на корректность ввода страны
    return bool(text)


# Обработчик для команды /start
@router.message(Command(commands=["start"]))
async def Start_handler(message: Message, state: FSMContext):
    # Вызываем функцию для обработки команды /start в базе данных
    await db.cmd_start_db(message.from_user.id, message.from_user.username)
    await state.set_state(Bot.start)
    if message.from_user.id == int(config.admin_alex_id):
        await message.answer(
            "Вы авторизовались как администратор!",
            reply_markup=kb.admin_panel
        )
        await state.set_state(Bot.admin_panel)
    else:
        await message.answer(text.greet.format(
            name=message.from_user.full_name),
            reply_markup=kb.start_keyboard
        )


# Обработчик для текста "Начать поиск работы!"
@router.message(Text(text=text.start_search_job))
async def Fillform_command(message: Message, state: FSMContext):
    keyboard = types.ReplyKeyboardRemove()
    await message.answer(
        text='Пожалуйста введите желаемую должность ',
        reply_markup=keyboard
    )
    await state.set_state(Resume.job)


# В обработчике для ввода должности
@router.message(StateFilter(Resume.job))
async def job_sent(message: Message, state: FSMContext):
    user_id = message.from_user.id
    job = message.text

    if not is_valid_job(job):
        await message.answer("Пожалуйста, введите корректную должность!")
        return

    user_data_dict[user_id] = {
        'job': job,
        'salary': None,
        'country': None,
        'town': None,
    }

    await message.answer(text='Спасибо!\n\nА теперь введите желаемую заработную плату:')
    await state.set_state(Resume.salary)


# Обработчик для сообщений в состоянии Ввода желаемой работы
@router.message(StateFilter(Resume.job))
async def salary_sent(message: Message, state: FSMContext):
    await state.update_data(job=message.text)
    await state.set_state(Resume.salary)


# Обработчик для сообщений в состоянии Введите желаемую зарплату
@router.message(StateFilter(Resume.salary))
async def salary_sent(message: Message, state: FSMContext):
    user_id = message.from_user.id
    salary = message.text

    # Проверяем данные на "дурака"
    if not is_valid_salary(salary):
        await message.answer("Пожалуйста, введите корректную зарплату (положительное число)!")
        return

    user_data = user_data_dict.get(user_id, {})
    user_data['salary'] = salary
    user_data_dict[user_id] = user_data

    await state.update_data(salary=salary)
    await message.answer(text='И последнее перед тем как найти вам работу, введите вашу Страну:')
    await state.set_state(Resume.country)


# Обработчик для сообщений в состоянии Введите желаемую зарплату
@router.message(StateFilter(Resume.salary))
async def town_sent(message: Message, state: FSMContext):
    await state.update_data(salary=message.text)
    await state.set_state(Resume.country)


# Обработчик для ввода страны
@router.message(StateFilter(Resume.country))
async def country_sent(message: Message, state: FSMContext):
    user_id = message.from_user.id
    country = message.text

    # Проверьте данные на "дурака"
    if not is_valid_country(country):
        await message.answer("Пожалуйста, введите корректную страну!")
        return

    # Сохраните страну в данных пользователя
    user_data = user_data_dict.get(user_id, {})
    user_data['country'] = country
    user_data_dict[user_id] = user_data

    await state.update_data(country=country)
    await message.answer(text='Теперь введите ваш город:')
    await state.set_state(Resume.town)


# Функция для форматирования города с тире
def format_city_name(city_name):
    # Разбиваем город на слова и форматируем каждое слово
    formatted_words = [word.capitalize() for word in city_name.split()]
    # Объединяем слова с тире между ними
    formatted_city = "-".join(formatted_words)
    return formatted_city


# Обработчик для сообщений в состоянии Введите ваш город
@router.message(StateFilter(Resume.town))
async def town_sent(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text_input = message.text

    # Форматируем город с тире
    town = format_city_name(text_input)

    # Проверяем данные на "дурака"
    if not is_valid_town(town):
        await message.answer("Пожалуйста, введите корректный город!")
        return

    user_data = user_data_dict.get(user_id, {})
    user_data['town'] = town
    user_data_dict[user_id] = user_data

    await state.update_data(town=town)
    await message.answer(text='Спасибо, теперь можно перейти в просмотр вакансий', reply_markup=kb.job_keyboard)
    await state.clear()


# Обработчик для кнопки перезапуска теста
@router.message(Text(text=text.re))
async def re_start(message: Message, state: FSMContext):
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("Вы начали процесс сбора данных заново.")
    await message.answer(text='Пожалуйста введите желаемую должность:', reply_markup=keyboard)
    await state.set_state(Resume.job)


async def country_name_to_code(country_name):
    async with aiohttp.ClientSession() as session:
        url = 'https://api.hh.ru/areas'
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                for area in data:
                    if area['name'] == country_name:
                        return area['id']
                print(f"Country name '{country_name}' not found in HH API data.")  # Отладочный вывод
            else:
                print(f"Error response from HH API: {response.status}")  # Отладочный вывод
            return None


async def city_name_to_code(city_name, country_name):
    async with aiohttp.ClientSession() as session:
        url = 'https://api.hh.ru/areas'
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                for country in data:
                    if country['name'] == country_name:
                        for area in country['areas']:
                            if area['name'] == city_name:
                                return area['id']
                print(
                    f"City name '{city_name}' not found in HH API data for country '{country_name}'.")  # Отладочный вывод
            else:
                print(f"Error response from HH API: {response.status}")  # Отладочный вывод
            return None


async def search_hh_vacancies(job, salary, country_code, area_code):
    async with aiohttp.ClientSession() as session:
        url = f'https://api.hh.ru/vacancies'
        params = {
            'text': job,
            'salary': salary,
            'area': area_code,
            'country': country_code
        }
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                vacancies = data.get('items', [])
                for vacancy in vacancies:
                    required_experience = vacancy.get('experience', {}).get('name', 'Не указано')
                    employment = vacancy.get('employment', {}).get('name', 'Не указано')
                    vacancy['required_experience'] = required_experience
                    vacancy['employment'] = employment
                return vacancies
            else:
                return None

user_vacancy_data = {}


def get_next_vacancy(user_id):
    user_data = user_vacancy_data.get(user_id, {})
    vacancies = user_data.get('vacancies', [])
    current_index = user_data.get('current_index', 0)

    if current_index < len(vacancies):
        return vacancies[current_index], current_index
    else:
        return None, None

def update_current_index(user_id, index):
    user_data = user_vacancy_data.get(user_id, {})
    user_data['current_index'] = index
    user_vacancy_data[user_id] = user_data

async def send_next_vacancy(user_id, message):
    vacancy, current_index = get_next_vacancy(user_id)
    if vacancy is not None:
        title = vacancy.get('name', 'Не указано')
        employer = vacancy.get('employer', {}).get('name', 'Не указано')
        salary = vacancy.get('salary', {}).get('from', 'Не указано')
        required_experience = vacancy.get('required_experience', 'Не указано')
        employment = vacancy.get('employment', 'Не указано')

        vacancy_message = f"<b>Название:</b> {title}\n" \
                          f"<b>Работодатель:</b> {employer}\n" \
                          f"<b>Зарплата от:</b> {salary}\n" \
                          f"<b>Требуемый опыт:</b> {required_experience}\n" \
                          f"<b>Занятость:</b> {employment}"

        await message.answer(vacancy_message, parse_mode='HTML')

        update_current_index(user_id, current_index + 1)
    else:
        await message.answer("Вы просмотрели все доступные вакансии.")




# Handler to start vacancy viewing
@router.message(Text(text=text.job))
async def check_handler(message: Message, state: FSMContext):
    await message.answer(text='Вот, что мы смогли подобрать', reply_markup=kb.live_check_job)
    user_id = message.from_user.id
    user_data = user_data_dict.get(user_id, None)
    job = user_data.get('job', 'Не указано')
    salary_min = int(user_data.get('salary', 20000))
    country = user_data.get('country', 'Не указано')
    town = user_data.get('town', 'Не указано')

    country_code = await country_name_to_code(country)
    area_code = await city_name_to_code(town, country)



    if country_code is None or area_code is None:
        await message.answer(
            f"Извините, название страны '{country}' или города '{town}' не распознано или не найдено в API HH.ru.")
        return

    vacancies = await search_hh_vacancies(job, salary_min, country_code, area_code)

    print("Job:", job)  # Отладочное сообщение
    print("Salary:", salary_min)  # Отладочное сообщение
    print("Town:", area_code)  # Отладочное сообщение
    print("Vacancies:", vacancies)  # Отладочное сообщение


    if vacancies:
        user_vacancy_data[user_id] = {'vacancies': vacancies, 'current_index': 0}
        await send_next_vacancy(user_id, message)
    else:
        await message.answer("Извините, ничего не найдено по вашему запросу.")


async def get_vacancy_url(vacancy_id):
    async with aiohttp.ClientSession() as session:
        url = f'https://api.hh.ru/vacancies/{vacancy_id}'
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('alternate_url')
            else:
                return None


# Обработчик для кнопки "Лайк"
@router.message(Text(text=text.like))
async def like_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = user_data_dict.get(user_id, {})
    vacancy, current_index = get_next_vacancy(user_id)
    if vacancy is not None:
        vacancy_id = vacancy.get('id')
        vacancy_url = await get_vacancy_url(vacancy_id)
        if vacancy_url:
            await message.answer(f"Вы лайкнули эту вакансию. Ссылка на вакансию: {vacancy_url}")
        else:
            await message.answer("Извините, не удалось получить ссылку на вакансию.")

        # Спрашиваем, хотите ли вы посмотреть следующую вакансию
        await message.answer("Хотите посмотреть следующую вакансию?", reply_markup=kb.yes_no_keyboard)
        update_current_index(user_id, current_index + 1)
    else:
        await message.answer("Вы просмотрели все доступные вакансии.")


# Обработчик для кнопки "Дизлайк"
@router.message(Text(text=text.dis))
async def dislike_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = user_data_dict.get(user_id, {})
    vacancy, current_index = get_next_vacancy(user_id)

    if vacancy is not None:
        await message.answer("Вы дислайкнули эту вакансию. Хотите посмотреть следующую?",
                             reply_markup=kb.yes_no_keyboard)

        # Переводим пользователя в состояние Dislike для ожидания дальнейших действий
        await state.set_state(Bot.dislike)
    else:
        await message.answer("Вы просмотрели все доступные вакансии.")


# Обработчик для кнопки "Да"
@router.message(Text(text=text.yes))
async def yes_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = user_data_dict.get(user_id, {})
    await message.answer("Обязательная заглушка(Можно сделать смайлик)", reply_markup=kb.live_check_job)
    # Проверяем, есть ли следующая вакансия
    vacancy, current_index = get_next_vacancy(user_id)
    if vacancy is not None:
        # Отправляем следующую вакансию
        await send_next_vacancy(user_id, message)
    else:
        await message.answer("Вы просмотрели все доступные вакансии.")
    # Сбрасываем состояние выбора "Да" или "Нет"
    await state.clear()



# Обработчик для кнопки "Нет"
@router.message(Text(text=text.no))
async def no_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    # Сбрасываем состояние выбора "Да" или "Нет"
    await state.clear()
    # Возвращаем пользователя в главное меню
    await message.answer("Вы можете в любой момент продолжить просмотр вакансий.", reply_markup=kb.job_keyboard)


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



