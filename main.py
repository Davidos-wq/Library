from models import User,Book,BorrowedBook,init_models
from database import async_session_factroy
import asyncio

from datetime import datetime

from aiogram import Bot,Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from os import getenv

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()

async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main)