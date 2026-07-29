from sqlalchemy import select
from models import Book,User,BorrowedBook
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import func,select
from sqlalchemy.orm import selectinload
from crud import found_book

async def move_page(session,command):

    builder = InlineKeyboardBuilder()
    PAGE_SIZE = 10

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
        nextpage = PAGE_SIZE+command
        builder.add(InlineKeyboardButton
                    (text="Вперед ➡️",callback_data=f"forward_{nextpage}")
                    )
    
    if command>=10:
        previouspage = command-PAGE_SIZE
        builder.add(InlineKeyboardButton(
                    text="⬅️ Назад",callback_data=f"back_{previouspage}"))
    
    builder.adjust(2)

    return builder.as_markup()

async def moveuser_page(session, command: int, tg_id: int):

    PAGE_SIZE = 10

    builder = InlineKeyboardBuilder()

    stmt = (
        select(BorrowedBook)
        .where(BorrowedBook.user_id == tg_id)
        .options(selectinload(BorrowedBook.book_info))
        .offset(command)
        .limit(PAGE_SIZE)
    )
    all_userbooks = (await session.execute(stmt)).scalars().all()

    count_stmt = select(func.count(BorrowedBook.id)).where(BorrowedBook.user_id == tg_id)
    total_userbooks = await session.scalar(count_stmt) or 0

    # 3. Додаємо книги у клавіатуру
    for book in all_userbooks:
        builder.add(InlineKeyboardButton(
            text=book.book_info.title,
            callback_data=f"showuserbook_{book.id}_{command}"
        ))

    builder.adjust(2)

    nav_builder = InlineKeyboardBuilder()

    if command >= PAGE_SIZE:
        prev_offset = command - PAGE_SIZE
        nav_builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"userback_{prev_offset}"))

    if command + PAGE_SIZE < total_userbooks:
        next_offset = command + PAGE_SIZE
        nav_builder.add(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"userforward_{next_offset}"))

    builder.attach(nav_builder)

    return builder.as_markup()

    


    