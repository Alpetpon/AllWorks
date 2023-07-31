from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
import text


router = Router()


# Обработчик комнды /start
@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    await message.answer(text.greet.format(name = message.from_user.full_name))

# Обработчик команды /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text.help)


