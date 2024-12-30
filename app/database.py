
import os
import pymysql
from aiomysql import create_pool
from aiomysql.pool import Pool
from datetime import *
import json
db_pool: Pool | None = None


async def init_db():
    global db_pool
    db_pool = await create_pool(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        db=os.getenv("MYSQL_DATABASE"),
        autocommit=True,
    )
    print("Підключення до бази даних встановлено")


async def close_db():
    global db_pool
    if db_pool:
        db_pool.close()
        await db_pool.wait_closed()
        print("Підключення до бази даних закрито")


def execute_query_sync(query, params=None):
    connection = pymysql.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        autocommit=True,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
    finally:
        connection.close()


async def execute_query(query, params=None, fetch="fetchall"):
    global db_pool
    if not db_pool:
        raise RuntimeError("Database pool is not initialized")
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params or ())
            if query.strip().lower().startswith("select") and fetch == "fetchall":
                return await cur.fetchall()
            elif query.strip().lower().startswith("select") and fetch == "fetchone":
                return await cur.fetchone()




async def create_tables():
    execute_query_sync("""
        CREATE TABLE IF NOT EXISTS users_profile (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255)
        )
    """)
    execute_query_sync("""
        CREATE TABLE IF NOT EXISTS profile_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            profile_name VARCHAR(255),
            profile_info VARCHAR(255)
        )
    """)
    execute_query_sync("""
        CREATE TABLE IF NOT EXISTS rezult_profile
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),
            result JSON
    """)
    execute_query_sync("""
        CREATE TABLE IF NOT EXISTS time_vizit
            id INT AUTI_INCREMENT PRIMARY KEY,
            photo_id VARCHAR(255)
    """)

    print("Таблиці створено або вже існують")

async def remember_me(user_id):
    global db_pool
    if not db_pool:
        raise RuntimeError("Database pool is not initalized")
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                INSERT INTO users_profile (user_id) VALUES(%s)
            """, (user_id,))
async def get_profiles():
    global db_pool
    if not db_pool:
        raise RuntimeError("Database pool is not initalized")
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute_query("""
                SELECT * FROM profile_info
            """)