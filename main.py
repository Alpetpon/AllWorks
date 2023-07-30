import asyncio
import logging
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from config import BOT_TOKEN
from handlers import router


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Приветствую, <b>{message.from_user.full_name}!</b> Я помогу тебя в поиске работы мечты")




async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(BOT_TOKEN, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())