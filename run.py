import asyncio
import os
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
from app.handllers import router
from app.database import init_db, close_db, create_tables

load_dotenv()
bot = Bot(token=os.getenv("API_TOKEN"))


dp = Dispatcher()


async def on_startup():

    print("Бот успішно запущений")
    await init_db()
    await create_tables()


async def on_shutdown():

    print("Бот зупиняється...")
    await close_db()


async def main():

    dp.include_router(router)
    await on_startup()
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
