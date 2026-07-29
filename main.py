import asyncio
from aiogram import Bot,Dispatcher
from project_run.registration import form_router
from models import init_models,init_db

import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from showcase.main_menu import menu_router
from showcase.Userbooks.callback_queryes import userbook_router
from showcase.fastcomands import fastcomand_router

dotenv_path = find_dotenv()
print(f"DEBUG: Файл .env знайдено за шляхом: {dotenv_path}")

load_dotenv(dotenv_path, override=True)

token = os.getenv("BOT_TOKEN")
print(f"DEBUG: Значення BOT_TOKEN: '{token}'")

if not token:
    print("ПОМИЛКА: Змінну BOT_TOKEN не знайдено!")

dp = Dispatcher()

async def main() -> None:
    await init_models()
    await init_db()

    dp.include_router(form_router)
    dp.include_router(menu_router)
    dp.include_router(fastcomand_router)
    dp.include_router(userbook_router)
    
    bot = Bot(token=token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())