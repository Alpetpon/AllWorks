import asyncio  # для асинхронного запуска бота
import logging  # для настройки логгирования, которое поможет в отладке
import config # для хранении конфигурации бота
from aiogram import Bot, Dispatcher # основной модуль библиотеки aiogram
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode
from handlers import router # основной файл, в котором будет содержать почти весь код бота. Будет состоять из
# функций-обработчиков с декораторами (фильтрами)

async def main():
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
