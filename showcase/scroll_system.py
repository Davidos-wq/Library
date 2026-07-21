from sqlalchemy import select
from models import Book
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

page_load = 0

async def move_page(messege_id):
    stmt = (select(Book.title).
            offset(page_load).
            limit(10))