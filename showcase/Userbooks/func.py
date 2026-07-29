from sqlalchemy import select
from models import User,Book,BorrowedBook
from sqlalchemy.orm import selectinload
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from sqlalchemy import delete

# Показати інформацію про книжку юзера
async def showbook_info(session,book_id,message:Message):
    stmt = (select(BorrowedBook)
            .where(BorrowedBook.id==book_id).
            options(selectinload(BorrowedBook.book_info))
            )

    result = await session.execute(stmt)
    book_res = result.scalar_one_or_none()

    if book_res==None:
        await message.answer("Нараз id книжки не знайдено")
        return


    response_text = (
                f"<b>Книгу знайдено!</b>\n\n"
                f"<b>Назва:</b> {book_res.book_info.title}\n"
                f"<b>Автор:</b> {book_res.book_info.author}\n"
                f"<b>Рік:</b> {book_res.book_info.year}\n"
                f"<b>Жанр:</b> {book_res.book_info.genre}"
            )

    keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                        [
                        InlineKeyboardButton(
                            text="Повернутися",
                            callback_data=f"touserbook")
                        ]
                    ]
                )

    await message.answer(response_text,reply_markup=keyboard,parse_mode="HTML")

#Видалити книжку юзера
async def delete_userbook(session,book_id):

    stmt = delete(BorrowedBook).where(BorrowedBook.id==book_id)
    await session.execute(stmt)
    await session.commit()




