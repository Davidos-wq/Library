from showcase.Userbooks.markups import retur_userbook,agreement
from showcase.Userbooks.func import showbook_info,delete_userbook
from showcase.scroll_system import moveuser_page

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
   await state.update_data(page_num=int(book_id[2]))

   await callback.message.edit_text(text="Книжка користувача",
    reply_markup=retur_userbook())

@userbook_router.callback_query(F.data=="OpenBook")
async def open_book(callback:CallbackQuery,state:FSMContext):
   data = await state.get_data()  
   saved_book_id = data.get("book_id")

   async with async_session_factroy() as session:
      await showbook_info(session,saved_book_id,callback.message)

@userbook_router.callback_query(F.data=="touserbook")
async def returnto_usermenu(callback:CallbackQuery):
   await callback.message.edit_text(text="Книжка користувача",reply_markup=retur_userbook())

@userbook_router.callback_query(F.data=="Delete")
async def delete_book(callback:CallbackQuery):
   await callback.message.edit_text(text="Погодження",reply_markup=agreement())

@userbook_router.callback_query(F.data=="Agree")
async def agree_delete(callback:CallbackQuery,state:FSMContext):
   data = await state.get_data()  
   saved_book_id = data.get("book_id")
   saved_pagenum = data.get("page_num")

   async with async_session_factroy() as session:
    await delete_userbook(session,saved_book_id)
    await callback.message.edit_text(text="Книжки користувача",
                                     reply_markup=await moveuser_page(session,saved_pagenum,
                                                                callback.from_user.id))

    await state.clear()

@userbook_router.callback_query(F.data=="Disagree")
async def decline_delete(callback:CallbackQuery,state:FSMContext):
   await callback.message.edit_text(text="Книжка користувача",reply_markup=retur_userbook())


@userbook_router.callback_query(F.data=="Back")
async def back_userbookmenu(callback:CallbackQuery,state:FSMContext):
   data = await state.get_data()  
   saved_pagenum = data.get("page_num")
   
   async with async_session_factroy() as session:
    await callback.message.edit_text(text="Книжки користувача",reply_markup= await 
                                        moveuser_page(session,saved_pagenum,
                                                      callback.from_user.id))

   await state.clear()