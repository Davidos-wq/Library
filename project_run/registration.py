from models import User,Book,BorrowedBook,init_models
from aiogram.types import Message,CallbackQuery
from aiogram import Bot,Router
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from project_run.registrationbuttons import get_my_keyboard
from crud import add_info
from database import async_session_factroy
from aiogram import F
from showcase.main_menu import create_menu

form_router = Router()

class Form(StatesGroup):
    name = State()
    lastname = State()

@form_router.message(CommandStart())
async def message_handler(message: Message,state:FSMContext):
    await message.answer("Вітаємо читачу Введіть своє ім'я")
    await state.set_state(Form.name)

@form_router.message(Form.name)
async def process_name(message:Message,state:FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введіть своє прізвище")
    await state.set_state(Form.lastname)

@form_router.message(Form.lastname)
async def process_lastname(message:Message,state:FSMContext):
    await state.update_data(lastname=message.text)
    await message.answer("Виберіть ваший улюблений жанр із запропонованих",reply_markup=get_my_keyboard())

@form_router.callback_query(F.data.in_(["Science Fiction","Fantasy",
                                        "Mystery","Romance","Horror",
                                        "Literary Fiction"]))
async def process_genre(callback:CallbackQuery,state:FSMContext):
  
    all_data = await state.get_data() # Всі тимчасові збережені зміни
    user_id = callback.from_user.id

    name = all_data.get("name")
    lastname = all_data.get("lastname")
    genre = callback.data
    
    async with async_session_factroy() as session:
        await add_info(session,user_id,
                       name,lastname,genre)
    
    await callback.message.answer("Меню",reply_markup=create_menu())
    

        
    

    

    
    