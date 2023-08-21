import logging
import openai
from aiogram import Bot, Dispatcher, types

# Ваш токен бота от BotFather в Telegram
BOT_TOKEN = '6020728592:AAGReqJ2EgyvWSh_IM3zG-GdZFOb92gx9S0'

# Ваш API-ключ для GPT-3.5 Turbo от OpenAI
OPENAI_API_KEY = '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'

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Инициализация API OpenAI
openai.api_key = OPENAI_API_KEY

# Объявление словаря для хранения данных пользователя
user_data = {}

# Список полей, которые необходимо запросить у пользователя
fields = [
    "имя", "фамилия", "отчество", "желаемая должность", "опыт работы", "образование", "навыки"
]

# Индекс текущего запрашиваемого поля
current_field_index = 0

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    global current_field_index
    current_field_index = 0
    user_data.clear()

    await message.answer(f"Привет! Пожалуйста, введите {fields[current_field_index]}:")

# Обработчик всех остальных сообщений
@dp.message_handler()
async def handle_user_input(message: types.Message):
    global current_field_index

    user_input = message.text
    user_data[fields[current_field_index]] = user_input

    if current_field_index < len(fields) - 1:
        current_field_index += 1
        await message.answer(f"Введите {fields[current_field_index]}:")
    else:
        await generate_resume(message)

# Функция для генерации резюме
async def generate_resume(message: types.Message):
    try:
        # Собираем введенные данные в одну строку
        user_input = "\n".join([f"{field}: {user_data[field]}" for field in fields])

        # Создаем чат-сессию с системным сообщением и введенными данными пользователя
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a resume generation assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        resume = response.choices[0].message["content"]
    except Exception as e:
        resume = "Произошла ошибка при генерации резюме."

    await message.answer(resume)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
