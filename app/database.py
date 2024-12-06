import sqlite3 as sq

with sq.connect('app/profile.db') as con:
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    name TEXT,
    username TEXT,
    email TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS info(
    user TEXT,
    favourite_subj TEXT,
    answers TEXT,
    result TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS profile(
    profile_name TEXT,
    profile_info TEXT
    )
    """)


con = sq.connect('app/profile.db')
cur = con.cursor()

async def add_user_on_start(user_id, user_name, username):
    user = cur.execute("SELECT * FROM accounts WHERE user_id = ?", (user_id,)).fetchone()
    if not user:
        cur.execute("""
        INSERT INTO accounts (user_id, name, username) VALUES (?, ?, ?)
        """, (user_id, user_name, username))
        con.commit()

async def add_profile( profile_name, profile_info):
    profile = cur.execute("SELECT * FROM accounts WHERE user_id = ?", (profile_name,)).fetchone()
    if not profile:
        cur.execute("""
            INSERT INTO profile ( profile_name, profile_info) VALUES (?, ?)
            """, ( profile_name, profile_info))
        con.commit()

async def get_profiles():
    with sq.connect('app/profile.db') as con:
        con.row_factory = sq.Row  # Повертаємо словники
        cur = con.cursor()

        cur.execute("""
        SELECT * FROM profile
        """)
        profiles = cur.fetchall()  # Отримуємо результати
        return profiles

async def add_subj(answer, user_id):
    user = cur.execute("SELECT * FROM info WHERE user = ?", (user_id,)).fetchone()
    if not user:
        cur.execute("""
            INSERT INTO info (user, favourite_subj) VALUES (?, ?)
            """, (user_id, answer))
        con.commit()


# async def check_for_log(user_id, message):
#     user = cur.execute("SELECT * FROM accounts WHERE user_id = ?", (user_id,)).fetchone()
#     print("1")
#     if user is None:
#         answer = "Це знову ви?"
#
#
#         await message.answer(answer)
#         con.commit()