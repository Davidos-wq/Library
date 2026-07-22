from sqlalchemy import select
from models import Book
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def move_page(session,command):

    builder = InlineKeyboardBuilder()

    stmt = (select(Book.title).
            offset(command).
            limit(10))
    
    all_books = await session.execute(stmt)
    all_books = all_books.scalars().all()

    for book in all_books:
        builder.add(InlineKeyboardButton
                    (text=book,callback_data=f"item_{book}")
                    )
    
    if command<20:
        builder.add(InlineKeyboardButton
                    (text="Вперед",callback_data=f"forward_{command}")
                    )
    
    if command>=10:
        builder.add(InlineKeyboardButton(
                    text="Назад",callback_data=f"back_{command}"))
    
    builder.adjust(2)

    return builder.as_markup()
    

