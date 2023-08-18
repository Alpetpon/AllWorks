from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.filters.command import Command
from aiogram.types import Message
import text
import kb

router = Router()


class Search(StatesGroup):
    start = State()  # Стартовая позиция
    hub_choose_spec = State()  # Выбор специальности
    hub_create_resume = State()  # Cоздание резюме
    hub_choose_job = State()  # Оценка вакансий
    create_resume = State()  # Создание резюме


class resume(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()


# Обработчик комнды /start
@router.message(Command(commands=["start"]))
async def process_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Search.start)
    await message.answer(text.greet.format(name=message.from_user.full_name), reply_markup=kb.keyboard_prof)


# Обработчик команды /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text.help.format(name=message.from_user.full_name))


# Обработичк нажатия кнопки для перехода к вакансиям
@router.message(Text(text=text.prof_false))
async def process_prof_false_hendler(message: Message, state: FSMContext) -> None:
    await state.set_state(Search.hub_choose_spec)
    await message.answer(text.job_text.format(name=message.from_user.full_name), reply_markup=kb.keyboard_job_1)


# Обработичк нажатия кнопки выбора специализации
@router.message(Text(text=text.spis))
async def process_create_resume_hendler(message: Message, state: FSMContext) -> None:
    await state.set_state(Search.hub_create_resume)
    await message.answer(text.resume, reply_markup=kb.keyboard_job_2)


@router.message(Text(text=text.check_job))
async def process_check_job(message: Message, state: FSMContext) -> None:
    await state.set_state(Search.hub_choose_job)
    await message.answer(text.test, reply_markup=kb.keyboard_job_3)


@router.message(Text(text=text.create_resume))
async def process_create_resume(message: Message, state: FSMContext) -> None:
    await state.set_state(Search.create_resume)
    await message.answer("Введите свое имя:")
    await message.answer("Резюме успешно создано! Теперь выберите следующее действие.", reply_markup=kb.keyboard_job_3)


# Обработчик кнопки "Назад"
@router.message(lambda message: message.text == text.back)
async def process_back_button(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == Search.hub_create_resume:
        await state.set_state(Search.hub_choose_spec)
        await message.answer("Вы вернулись к выбору специальности.", reply_markup=kb.keyboard_job_1)
    elif current_state == Search.hub_choose_job:
        await state.set_state(Search.hub_create_resume)
        await message.answer("Вы вернулись к созданию резюме.", reply_markup=kb.keyboard_job_2)
    else:
        await message.answer("Нет такого состояния")
