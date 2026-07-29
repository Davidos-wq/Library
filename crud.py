from sqlalchemy import select,delete,func
from sqlalchemy import or_,text
from sqlalchemy.orm import joinedload,selectinload,with_loader_criteria
from models import Book,User,BorrowedBook
from sqlalchemy.exc import NoResultFound
from datetime import datetime
import time
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton


async def add_info(session,user_id,
                   username,lastname,genre):
    
    stmt = select(User).where(User.tg_id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        user.tg_id = user_id
        user.name = username
        user.lastname = lastname
        user.loved_genre = genre
    
    else:
        user = User(tg_id=user_id,name=username,
                    lastname=lastname,loved_genre=genre)
        
        session.add(user)  
    await session.commit()


from sqlalchemy import select, text
from aiogram.types import Message

async def found_book(session, book_title: str, message: Message) -> bool:
    stmt = select(Book).where(Book.title.ilike(book_title))
    result = await session.execute(stmt)
    book = result.scalar_one_or_none()

    if book:
        response_text = (
            f"<b>Книгу знайдено!</b>\n\n"
            f"<b>Назва:</b> {book.title}\n"
            f"<b>Автор:</b> {book.author}\n"
            f"<b>Рік:</b> {book.year}\n"
            f"<b>Жанр:</b> {book.genre}"
        )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                    [
                    InlineKeyboardButton(
                        text=book_title,
                        callback_data=f"item_{book.id}")
                    ]
                ]
            )
        await message.answer(response_text,reply_markup=keyboard,
                             parse_mode="HTML")
        return True 

    stmt = (
        select(Book)
        .where(Book.title.op('%')(book_title))
        .order_by(text("title <-> :query"))
        .params(query=book_title)
        .limit(5)
    )

    result = await session.execute(stmt)
    found_books = result.scalars().all()

    if not found_books:
        await message.answer("Книгу не знайдено. Спробуйте ввести іншу назву:")
        return False 

    suggestions = ["<b>Можливо, ви мали на увазі:</b>"]
    for b in found_books:
        suggestions.append(f"• {b.title} ({b.author})")
    
    suggestions.append("\nСпробуйте ввести назву ще раз:")

    await message.answer("\n".join(suggestions), parse_mode="HTML")
    return False 


async def add_book(session,tg_id,book_query,message:Message):
    
    book_id = int(book_query.split("_")[1])

    borowed_books = select(BorrowedBook.time_end).where(BorrowedBook.book_id==book_id)
    existing_borrow = (await session.execute(borowed_books)).scalar_one_or_none()

    if not existing_borrow or existing_borrow<datetime.now():

        new_borrow = BorrowedBook(
            user_id=int(tg_id),
            book_id=book_id
        )

        session.add(new_borrow)
        await session.commit()

        await message.answer('Книга була додана до вашої біліотеки')

    else:
        await message.answer('Наразі книга недоступна')


