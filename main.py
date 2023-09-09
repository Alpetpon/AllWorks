import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router
from set_menu import set_main_menu
import Database as db

# Асинхронная функция для запуска бота
async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(BOT_TOKEN, parse_mode="HTML")
    await set_main_menu(bot)  # Устанавливаем главное меню бота
    await dp.start_polling(bot)  # Запускаем бота в режиме "поллинга" (постоянной проверки новых сообщений)

# Асинхронная функция для инициализации базы данных и вывода сообщения об успешном запуске
async def on_data():
    await db.db_start()  # Инициализируем базу данных
    print("Бот успешно запущен")

# Асинхронная функция для запуска бота в цикле событий asyncio
async def run_bot():
    logging.basicConfig(level=logging.INFO)  # Настройка логирования
    await on_data()  # Вызываем функцию инициализации базы данных
    await main()  # Запускаем основную функцию бота

# Точка входа в программу
if __name__ == "__main__":
    asyncio.run(run_bot())  # Запускаем бота с использованием asyncio



