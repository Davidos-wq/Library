from sqlalchemy import select
from models import Book,User,BorrowedBook
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
from showcase.scroll_system import moveuser_page

def retur_userbook():

    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="Видалити",
                                      callback_data=f"Delete"))
    
    keyboard.add(InlineKeyboardButton(text="Показати інформацію",
                                      callback_data="OpenBook"))

    keyboard.add(InlineKeyboardButton(text="Назад",callback_data="Back"))

    keyboard.adjust(2)

    return keyboard.as_markup()


def agreement():

    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="Погодитися",callback_data="Agree"))
    keyboard.add(InlineKeyboardButton(text="Відмовитися",callback_data="Disagree"))

    keyboard.adjust(2)

    return keyboard.as_markup()

async def delete(session,book_id,message:Message,num):

    book = await session.get(BorrowedBook,book_id)
    await session.delete(book)
    await session.commit()

    user_id = int(message.from_user.id)

    await message.edit_text(text="Книжки",reply_markup=moveuser_page(session,num,user_id))

