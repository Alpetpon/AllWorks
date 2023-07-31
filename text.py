from aiogram.types import message
greet = f"Приветствую, <b>{message.from_user.full_name}!</b> Я помогу тебя в поиске работы мечты"
help  = f"<b>{message.from_user.full_name}!</b>, Если у тебя возникли вопросы, вот список базовых вопросов"