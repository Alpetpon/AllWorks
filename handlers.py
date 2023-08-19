from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.filters.command import Command
from aiogram.types import Message
import text, kb, config
import Database as db


router = Router()


class Search(StatesGroup):
    start = State()  # Стартовая позиция
    hub_choose_spec = State()  # Выбор специальности
    hub_create_resume = State()  # Cоздание резюме
    hub_choose_job = State()  # Оценка вакансий
    create_resume = State()  # Создание резюме
    admin_panel = State() # Панель админа бота


class resume(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()


# Обработчик команды /start
@router.message(Command(commands=["start"]))
async def Start_handler(message: Message, state: FSMContext):
    cur = db.db.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = cur.fetchone()
    if message.from_user.id == int(config.admin_alex_id):
        await message.answer("Вы авторизовались как администратор!", reply_markup= kb.admin_panel)
        await state.set_state(Search.admin_panel)
    else:
        if result is None:
            cur = db.db.cursor()
            cur.execute(f'''SELECT * FROM users WHERE (user_id="{message.from_user.id}")''')
            entry = cur.fetchone()
            if entry is None:
                cur.execute(f'''INSERT INTO users VALUES ('{message.from_user.id}', '0')''')
                db.db.commit()
                await message.answer(text.greet.format(name=message.from_user.full_name),
                                     reply_markup=kb.start_keyboard)
        else:
            await message.answer('Ты был заблокирован!')


# Обработчик создания резюме или просмотра вакансий
@router.message(Text(text=text.start_search_job))
async def Main_hendler(message: Message, state: FSMContext) -> None:
    await state.set_state(Search.hub_create_resume)
    await message.answer(text.resume, reply_markup=kb.Main_keyboard)

# Обработчик просмотра вакансий без создания резюме
@router.message(Text(text=text.check_job))
async def process_check_job(message: Message, state: FSMContext) -> None:
    await state.set_state(Search.hub_choose_job)
    await message.answer(text.test, reply_markup=kb.live_check_job)

# Обработчик создания резюме вручную
@router.message(Text(text=text.create_resume))
async def process_create_resume(message: Message, state: FSMContext) -> None:
    await state.set_state(Search.create_resume)
    await message.answer("Введите свое имя:")
    #TODO
    await message.answer("Резюме успешно создано! Теперь выберите следующее действие.", reply_markup=kb.live_check_job)


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


# Пока не нужно
""""
### Обработичк нажатия кнопки для перехода к выбору специальностей
@router.message(Text(text=text.))
async def Search_Handler(message: Message, state: FSMContext):
    await state.set_state(Search.hub_choose_spec)
    await message.answer(text.job_text.format(name=message.from_user.full_name), reply_markup=kb.keyboard_job_1)
"""

# Обработчик команды /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text.help.format(name=message.from_user.full_name))

@router.message(Command(commands = ['id']))
async def cmd_id(message: Message):
    await message.answer(f'{message.from_user.id}')


# обработчик Админ-Панели
@router.message(Text(text = text.admin))
async def Admin_panel(message: Message):
    if message.from_user.id == int(config.admin_alex_id):
        await message.answer(text.admin_panel, reply_markup = kb.Main_panel)

# Собираем статистику бота
@router.message(Text(text=text.stat))
async def hfandler(message: Message, state: FSMContext):
    cur = db.db.cursor()
    cur.execute('''select * from users''')
    results = cur.fetchall()
    await message.answer(f'Людей которые когда либо заходили в бота: {len(results)}')