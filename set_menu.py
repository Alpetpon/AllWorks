from aiogram import Bot
from aiogram.types import BotCommand
from lexicon_ru import LEXICON_COMMANDS_RU

# Асинхронная функция для настройки главного меню бота
async def set_main_menu(bot: Bot):
    # Создаем список команд для главного меню бота
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command, description in LEXICON_COMMANDS_RU.items()]

    # Устанавливаем команды меню для бота
    await bot.set_my_commands(main_menu_commands)
