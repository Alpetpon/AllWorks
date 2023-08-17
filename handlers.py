from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.filters.command import Command
from aiogram.types import Message
import text
import kb

router = Router()

class ProfilingState(StatesGroup):
    start = State()         # Начальное состояние
    true_test = State()     # Состояние после нажатия на кнопку "Пройти тест"
    continue_test = State() # Состояние после нажатия на кнопку "Продолжить"
    back = State()          # Состояние после нажатия на кнопку "Назад"
    restart = State()       # Состояние после нажатия на кнопку "Пройти заново"
    go_resume = State()     # Состояние после нажатия на кнопку "Перейти к резюме"

# Обработчик комнды /start
@router.message(Command(commands=["start"]))
async def process_start_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(current_state="start")
    await state.set_state(ProfilingState.start)
    await message.answer(text.greet.format(name=message.from_user.full_name), reply_markup=kb.keyboard_prof)

# Обработчик команды /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text.help.format(name=message.from_user.full_name))

# Обработчик нажатия кнопки для прохождения теста профориентации
@router.message(Text(text=text.prof_true))
async def process_prof_true_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(ProfilingState.true_test)
    await state.update_data(current_state="true_test")
    await message.answer(text.prof_text.format(name=message.from_user.full_name), reply_markup=kb.keyboard_prof_1)


# Обработичк нажатия кнопки продолжить в тесте
@router.message(Text(text = text.contin))
async def process_prof_continue_handler(message: Message) -> None:
    await message.answer(text.prof_answwer.format(name = message.from_user.full_name), reply_markup=kb.keyboard_prof_2)

# Обработчик нажатия кнопки "Назад"
@router.message(Text(text=text.back))
async def process_back_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    current_state = data.get("state", None)
    if current_state == "true_test":
        await state.set_state(ProfilingState.true_test)
        await message.answer("Вы вернулись в начальное состояние.", reply_markup=kb.keyboard_prof)
    elif current_state == "continue_test":
        await state.set_state(ProfilingState.continue_test)
        await message.answer("Вы вернулись к прохождению теста.", reply_markup=kb.keyboard_prof_1)
    elif current_state == "restart":
        await state.set_state(ProfilingState.restart)
        await message.answer("Вы вернулись к началу теста.", reply_markup=kb.keyboard_prof)
    elif current_state == "go_resume":
        await state.set_state(ProfilingState.go_resume)
        await message.answer("Вы вернулись в начальное состояние.", reply_markup=kb.keyboard_prof)
    elif current_state == "back":
        await state.set_state(ProfilingState.back)
        await message.answer("Вы вернулись к прохождению теста.", reply_markup=kb.keyboard_prof_1)
    else:
        await message.answer("Нет действий для возврата в данном состоянии.")

# Обработичк нажатия кнопки пройти занаво в тесте
@router.message(Text(text = text.reset))
async def process_prof_restart_handler(message: Message) -> None:
    await message.answer(text.prof_reset.format(name = message.from_user.full_name), reply_markup=kb.keyboard_prof_1)

# Обработичк нажатия кнопки перейти в  резюме
@router.message(Text(text = text.go_resum))
async def process_go_resume_handler(message: Message) -> None:
    await message.answer(text.block_job, reply_markup=kb.keyboard_job_2)

# Обработичк нажатия кнопки для перехода к вакансиям
@router.message(Text(text = text.prof_false))
async def process_prof_false_hendler(message: Message) -> None:
    await message.answer(text.job_text.format(name = message.from_user.full_name), reply_markup=kb.keyboard_job_1)

# Обработичк нажатия кнопки выбора специализации
@router.message(Text(text=text.spis))
async def process_create_resume_hendler(message: Message) -> None:
    await message.answer(text.resume, reply_markup=kb.keyboard_job_2)

@router.message(Text(text=text.check_job))
async def process_check_job(message: Message) -> None:
    await message.answer(text.test,reply_markup=kb.keyboard_job_3)