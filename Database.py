import sqlite3 as sq

db = sq.connect("client_base")
cur = db.cursor()

async def db_start():
    cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER, block INTEGER);""")
    db.commit()