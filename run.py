import asyncio
import os
from aiogram import Dispatcher, Bot
from app.handllers import router
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("API_TOKEN"))

dp = Dispatcher()

async def on_startup(_):
    print('Бот успішно запущений')

async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, on_startup=on_startup)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
