import asyncio
import logging
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from config import BOT_TOKEN
from handlers import router
import text

# Обработчик комнды /start
@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    await message.answer(text.greet)

# Обработчик команды /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text.help)


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(BOT_TOKEN, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())