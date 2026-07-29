from showcase.Userbooks.markups import retur_userbook,agreement,delete
from showcase.Userbooks.func import showbook_info,delete_userbook
from database import async_session_factroy 
from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram import F

userbook_router = Router()

@userbook_router.callback_query(F.data.startswith("showuserbook_"))
async def userbook_func(callback:CallbackQuery,state:FSMContext):
   book_id = callback.data.split("_")
   print(f"book_id:{book_id}")
   await state.update_data(book_id=int(book_id[1]))
   await callback.message.edit_reply_markup(
    reply_markup=retur_userbook())

@userbook_router.callback_query(F.data=="OpenBook")
async def open_book(callback:CallbackQuery,state):
   data = await state.get_data()  
   saved_book_id = data.get("book_id")

   async with async_session_factroy() as session:
      await showbook_info(session,saved_book_id,callback.message)
