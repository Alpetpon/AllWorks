from aiogram import Router, types
from aiogram.filters import Text
from aiogram.filters.command import Command
from aiogram.types import Message, ReplyKeyboardRemove
import text
import kb

router = Router()

# Обработчик комнды /start
@router.message(Command(commands=["start"]))
async def process_start_handler(message: Message) -> None:
    await message.answer(text.greet.format(name = message.from_user.full_name), reply_markup=kb.keyboard)

# Обработичк нажатия кнопки для прохождения теста профориентации
@router.message(Text(text = text.prof_true))
async def process_prof_true_hendler(message: Message) -> None:
    await message.answer(text.prof_text.format(name = message.from_user.full_name), reply_markup=ReplyKeyboardRemove())
# Обработичк нажатия кнопки для перехода к вакансиям
@router.message(Text(text = text.prof_false))
async def process_prof_false_hendler(message: Message) -> None:
    await message.answer(text.job_text.format(name = message.from_user.full_name), reply_markup=ReplyKeyboardRemove())

# Обработчик команды /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text.help)


