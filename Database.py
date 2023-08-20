import sqlite3 as sq

db = sq.connect("client_base")
cur = db.cursor()


async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "tg_id INTEGER, "
                "tg_username TEXT, "
                "resume_check TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS items("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT, "
                "surname TEXT, "
                "patronymic TEXT)")
    db.commit()


async def cmd_start_db(user_id, tg_username):
    user = cur.execute("SELECT * FROM accounts WHERE tg_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (tg_id, tg_username) VALUES ({key}, '{username}')".format(key=user_id,
                                                                                                    username=tg_username))
        db.commit()