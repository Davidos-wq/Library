from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,Message
from aiogram import Router
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

menu_router = Router()

def create_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Показати всі книжки",callback_data="show_all")
    builder.button(text="Знайти книгу",callback_data="found_book")
    builder.button(text="Взяти книгу",callback_data="get_book")
    builder.button(text="Повернути книгу",callback_data="return_book")
    builder.button(text="Подивитися свої книги",callback_data="show_yourbooks")

    builder.adjust(1)

    return builder.as_markup()


@menu_router.message(Command("show_menu"))
async def show_menu(message:Message):
      await message.answer("Меню вибору",reply_markup=create_menu())