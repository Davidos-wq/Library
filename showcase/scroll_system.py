from sqlalchemy import select
from models import Book,User,BorrowedBook
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import func,select
from sqlalchemy.orm import selectinload
from crud import found_book

async def move_page(session,command):

    builder = InlineKeyboardBuilder()

    stmt = (select(Book).
            offset(command).
            limit(10)) 
    
    all_books = await session.execute(stmt)
    all_books = all_books.scalars().all()

    count_stmt = select(func.count(Book.id))
    total_books = await session.scalar(count_stmt) # Підраховані книжки

    for book in all_books:
        builder.add(InlineKeyboardButton
                    (text=book.title,callback_data=f"item_{book.id}")
                    )
    
    if command<total_books-10:
        builder.add(InlineKeyboardButton
                    (text="Вперед",callback_data=f"forward_{command}")
                    )
    
    if command>=10:
        builder.add(InlineKeyboardButton(
                    text="Назад",callback_data=f"back_{command}"))
    
    builder.adjust(2)

    return builder.as_markup()

async def moveuser_page(session,command,tg_id):

    builder = InlineKeyboardBuilder()

    stmt = (select(User).
            where(User.tg_id==tg_id).
            options(
                selectinload(User.user_books).
                selectinload(BorrowedBook.book_info).
                offset(command).
                limit(10))
            )
            

    all_userbooks = await session.execute(stmt)
    all_userbooks = all_userbooks.scalar_one_or_none()

    count_stmt = (
    select(func.count(BorrowedBook.id))
    .where(BorrowedBook.user_id == all_userbooks.id))
    
    total_userbooks = await session.scalar(count_stmt)

    for book in all_userbooks.user_books:
        builder.add(InlineKeyboardButton(text=book.book_info.title,
                    callback_data=f"showuserbook_{book.id}"))

    if total_userbooks%10==0:
            builder.add(InlineKeyboardButton
                        (text="Вперед",callback_data=f"userforward_{command}")
                        )
    if command>=10:
            builder.add(InlineKeyboardButton(
                        text="Назад",callback_data=f"userback_{command}"))

    builder.adjust(2)
    
    return builder.as_markup()

    


    