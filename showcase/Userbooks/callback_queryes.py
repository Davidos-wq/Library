from showcase.Userbooks.markups import retur_userbook,agreement,delete
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
async def open_book()