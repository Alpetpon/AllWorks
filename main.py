import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router
from set_menu import set_main_menu
import Database as db

async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(BOT_TOKEN, parse_mode="HTML")
    await set_main_menu(bot)
    await dp.start_polling(bot)


async def on_data():
    await db.db_start()
    print("Бот успешно запущен")


async def run_bot():
    logging.basicConfig(level=logging.INFO)
    await on_data()
    await main()

if __name__ == "__main__":
    asyncio.run(run_bot())
