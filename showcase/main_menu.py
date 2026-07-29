from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,Message,CallbackQuery
from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

from showcase.scroll_system import move_page,moveuser_page
from crud import found_book,add_book
from database import async_session_factroy

menu_router = Router()

class Found(StatesGroup):
   book_name = State()


def create_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Показати всі книжки",callback_data="showall_0")
    builder.button(text="Знайти книгу",callback_data="found_book")
    builder.button(text="Подивитися свої книги",callback_data="showyourbooks_0")

    builder.adjust(1)

    return builder.as_markup()


@menu_router.message(Command("show_menu"))
async def show_menu(message:Message):
      await message.answer("Меню вибору",reply_markup=create_menu())


@menu_router.callback_query(F.data == "found_book")
async def enter_book_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введіть назву вашої книги")
    await state.set_state(Found.book_name)
    await callback.answer()


@menu_router.message(Found.book_name)
async def show_result(message: Message, state: FSMContext):
    async with async_session_factroy() as session:
        is_found = await found_book(session, message.text, message)

    if is_found:
        await state.clear()

#Показує меню всіх книг
@menu_router.callback_query(F.data.startswith("showall_"))
async def show_books(callback: CallbackQuery):
  curent_data = callback.data.split("_")
  num = int(curent_data[1])  # Тут буде 0 (або інше число, якщо передасте далі)

  async with async_session_factroy() as session:
    await callback.message.answer(
        text="Книжки",
        reply_markup=await move_page(session, num),
    )

  await callback.answer()

#Показує меню користувача книг
@menu_router.callback_query(F.data.startswith("showyourbooks_"))
async def showuser_book(callback:CallbackQuery):
   curent_data = callback.data.split("_")
   num = int(curent_data[1])

   async with async_session_factroy() as session:
      await callback.message.answer(text="Книжки користувача",
                                   reply_markup=await moveuser_page(session,num,callback.from_user.id))

   await callback.answer()
      
#Рухає меню каталогу всіх книг
@menu_router.callback_query(F.data.startswith(("forward_", "back_")))
async def front_move(callback: CallbackQuery):
  curent_data = callback.data.split("_")
  num = int(curent_data[1])

  # if curent_data[0] == "forward":
  #   num += 10
  # elif curent_data[0] == "back":
  #   num -= 10

  async with async_session_factroy() as session:
    await callback.message.edit_text(
        text="Книжки",
        reply_markup= await move_page(session, num),
    )

  await callback.answer()

#Рухає меню книг користувача
@menu_router.callback_query(
      F.data.contains("userforward_") | F.data.contains("userback_"))
async def user_move(callback:CallbackQuery):
  curent_data = callback.data.split("_")
  num = int(curent_data[1])

  async with async_session_factroy() as session:
    await callback.message.edit_text(
        text="Книжки",
        reply_markup= await moveuser_page(session, num,int(callback.from_user.id)),
    )

  await callback.answer()


@menu_router.callback_query(F.data.contains("item_"))
async def update_info(callback:CallbackQuery):
  async with async_session_factroy() as session:
     await add_book(session,callback.from_user.id,
              callback.data,callback.message)




# @menu_router.callback_query(F.data=="OpenBook")
# async def open_book(callback:CallbackQuery,state:FSMContext):
   