# Импортируем необходимые модули из библиотеки aiogram
from aiogram import Router, F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.types import Message

# Импортируем  модули необходимые для работы
import text, kb, config
import Database as db

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

# Обработчик для команды /start
@router.message(Command(commands=["start"]))
async def Start_handler(message: Message, state: FSMContext):
    # Вызываем функцию для обработки команды /start в базе данных
    await db.cmd_start_db(message.from_user.id, message.from_user.username)
    await state.set_state(Bot.start)
    if message.from_user.id == int(config.admin_alex_id):
        await message.answer("Вы авторизовались как администратор!", reply_markup= kb.admin_panel)
        await state.set_state(Bot.admin_panel)
    else:
        await message.answer(text.greet.format(name=message.from_user.full_name), reply_markup=kb.start_keyboard)

# Обработчик для текста "Начать поиск работы!"
@router.message(Text(text=text.start_search_job))
async def Fillform_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста введите желаемую должность ', reply_markup=kb.Back)
    await state.set_state(Bot.set_job)
    await state.set_state(Resume.job)

# Обработчик для сообщений в состоянии Ввода желаемой работы
@router.message(StateFilter(Resume.job))
async def salary_sent(message: Message, state: FSMContext):
    await state.update_data(job=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите желаемую заработную плату ')
    await state.set_state(Bot.set_salary)
    await state.set_state(Resume.salary)

# Обработчик для сообщений в состоянии Введите желаемую зарплату
@router.message(StateFilter(Resume.salary))
async def town_sent(message: Message, state: FSMContext):
    await state.update_data(salary=message.text)
    await message.answer(text='И последнее перед тем как натйи ввам работу,введите ваш город')
    await state.set_state(Bot.set_town)
    await state.set_state(Resume.town)

# Обработчик для сообщений в состоянии  Введите ваш город
@router.message(StateFilter(Resume.town))
async def close_test(message: Message, state: FSMContext):
    await state.update_data(town=message.text)
    await state.clear()
    await  message.answer(text='Спасибо, теперь можно перейти в просмотру вакансий', reply_markup=kb.job_keyboard)

# Обработчик для кнопки "Назад" еще не доделан
@router.message(lambda message: message.text == text.back)
async def process_back_button(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Bot.set_town:
        await state.set_state(Bot.set_salary)
    elif current_state == Bot.set_salary:
        await  state.set_state(Bot.set_job)
    else:
        await message.answer("Нет такого состояния")

# Обработчик для текста "Cмотреть вакансии ъ"
@router.message(Text(text=text.job))
async def check_hendler(message: Message):
    await message.answer(text.test, reply_markup=kb.live_check_job)

# Обработчик для команды /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text.help.format(name=message.from_user.full_name))

# Обработчик для команды /id
@router.message(Command(commands = ['id']))
async def cmd_id(message: Message):
    await message.answer(f'Твой id:{message.from_user.id}')

# Обработчик для текста "admin"
@router.message(Text(text = text.admin))
async def Admin_panel(message: Message):
    if message.from_user.id == int(config.admin_alex_id):
        await message.answer(text.admin_panel, reply_markup = kb.Main_panel)
