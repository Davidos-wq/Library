from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,Message
from aiogram import Router
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

menu_router = Router()




@menu_router.message(Command("show_menu"))
async def show_menu(message:Message):
