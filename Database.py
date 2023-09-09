# Импортируем модуль для работы с SQLite базой данных
import sqlite3 as sq

# Устанавливаем соединение с базой данных с именем "client_base"
db = sq.connect("client_base")

# Создаем курсор для выполнения SQL-запросов
cur = db.cursor()


# Асинхронная функция для инициализации базы данных
async def db_start():
    # Создаем таблицу "accounts", если она не существует
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "tg_id INTEGER, "
                "tg_username TEXT, "
                "resume_check TEXT)")

    # Создаем таблицу "items", если она не существует
    cur.execute("CREATE TABLE IF NOT EXISTS items("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT, "
                "surname TEXT, "
                "patronymic TEXT)")

    # Фиксируем изменения в базе данных
    db.commit()


# Асинхронная функция для начала работы с базой данных
async def cmd_start_db(user_id, tg_username):
    # Извлекаем информацию о пользователе по tg_id
    user = cur.execute("SELECT * FROM accounts WHERE tg_id == {key}".format(key=user_id)).fetchone()

    # Если пользователь не существует, добавляем его в базу данных
    if not user:
        cur.execute("INSERT INTO accounts (tg_id, tg_username) VALUES ({key}, '{username}')".format(key=user_id,
                                                                                                    username=tg_username))
        # Фиксируем изменения в базе данных
        db.commit()



