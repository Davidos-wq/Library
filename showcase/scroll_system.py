from sqlalchemy import select
from models import Book
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

page_load = 0

async def move_page(session,messege_id):

    builder = InlineKeyboardBuilder()

    stmt = (select(Book.title).
            offset(page_load).
            limit(10))
    
    all_books = await session.execute(stmt)
    all_books = all_books.scalars().all()

    for book in all_books:
        builder.add(InlineKeyboardButton
                    (text=book,callback_data=f"item_{book}")
                    )
    
    if page_load<20:
        builder.add(InlineKeyboardButton
                    (text="Вперед",callback_data="forward")
                    )
    
    if page_load>10:
        builder.add(InlineKeyboardButton(
                    text="Назад",callback_data="back"))
    
    builder.adjust(2)

    return builder.as_markup()
    

  