import asyncio
from aiogram import Bot,Dispatcher
from project_run.registration import form_router

from os import getenv

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()

async def main() -> None:
    dp.include_router(form_router)
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main)