from aiogram import Router, types
from aiogram.filters import Text
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import text
import kb

router = Router()

# Обработчик комнды /start
@router.message(Command(commands=["start"]))
async def process_start_handler(message: Message) -> None:
    await message.answer(text.greet.format(name = message.from_user.full_name), reply_markup=kb.keyboard_prof)

# Обработчик команды /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text.help.format(name = message.from_user.full_name))



#это код с гита. Кнопка назад. Мб сработает
@dp.callback_query_handler(text="Start")
async def start_callback(query: CallbackQuery):
    await query.message.edit_text(text=start_text, reply_markup=kb.keyboard)





# Обработичк нажатия кнопки для прохождения теста профориентации
@router.message(Text(text = text.prof_true))
async def process_prof_true_hendler(message: Message) -> None:
    await message.answer(text.prof_text.format(name = message.from_user.full_name), reply_markup=kb.keyboard_prof_1)

# Обработичк нажатия кнопки продолжить в тесте
@router.message(Text(text = text.contin))
async def process_prof_continue_handler(message: Message) -> None:
    await message.answer(text.prof_answwer.format(name = message.from_user.full_name), reply_markup=kb.keyboard_prof_2)

# Обработичк нажатия кнопки пройти занаво в тесте
@router.message(Text(text = text.reset))
async def process_prof_back_handler(message: Message) -> None:
    await message.answer(text.prof_reset.format(name = message.from_user.full_name), reply_markup=kb.keyboard_prof_1)

# Обработичк нажатия кнопки перейти в  резюме
@router.message(Text(text = text.go_resum))
async def process_go_resume_handler(message: Message) -> None:
    await message.answer(text.block_job, reply_markup=kb.keyboard_job_1)

# Обработичк нажатия кнопки для перехода к вакансиям
@router.message(Text(text = text.prof_false))
async def process_prof_false_hendler(message: Message) -> None:
    await message.answer(text.job_text.format(name = message.from_user.full_name), reply_markup=kb.keyboard_job_1)
# Обработичк нажатия кнопки выбора специализации
@router.message(Text(text=text.spis))
async def process_create_resume_hendler(message: Message) -> None:
    await message.answer(text.resume, reply_markup=kb.keyboard_job_2)

@router.message(Text(text=text.check_job))
async  def process_check_job(message: Message) -> None:
    await  message.answer(text.test,reply_markup=kb.keyboard_job_3)