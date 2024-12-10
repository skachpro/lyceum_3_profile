import asyncio
import os
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
from app.handllers import router
from app.database import init_db, close_db, create_tables  # Імпорт функцій для роботи з базою

load_dotenv()
bot = Bot(token=os.getenv("API_TOKEN"))

# Ініціалізація диспетчера
dp = Dispatcher()


async def on_startup():
    """Функція для запуску всіх необхідних процесів при старті бота."""
    print("Бот успішно запущений")
    await init_db()  # Ініціалізуємо підключення до бази даних
    await create_tables()  # Створюємо таблиці, якщо їх ще немає


async def on_shutdown():
    """Функція для завершення всіх процесів при зупинці бота."""
    print("Бот зупиняється...")
    await close_db()  # Закриваємо підключення до бази даних


async def main():
    """Основна функція для запуску бота."""
    dp.include_router(router)  # Підключаємо маршрутизатор
    await on_startup()  # Запускаємо стартові процеси
    try:
        await dp.start_polling(bot)  # Запускаємо лонг-полінг
    finally:
        await on_shutdown()  # Завершуємо всі процеси при зупинці


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
