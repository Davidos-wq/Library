from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message
from aiogram import F
from showcase.main_menu import create_menu

fastcomand_router = Router()


@fastcomand_router.message(Command("show_menu"))
async def show_menu(message:Message):
      await message.answer("Меню вибору",reply_markup=create_menu())

