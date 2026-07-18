from models import User,Book,BorrowedBook,init_models
from aiogram.types import Message,CallbackQuery
from aiogram import Bot,Router
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from registrationbuttons import get_my_keyboard

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
    await message.answer("Введіть своє прізвище")
    await state.set_state(Form.lastname)

@form_router.message(Form.lastname)
async def process_lastname(message:Message,state:FSMContext):
    await message.answer("Виберіть ваший улюблений жанр із запропонованих",reply_markup=get_my_keyboard())

@form_router.callback_query()
async def process_genre(callback:CallbackQuery,state:FSMContext):
    genre = callback.data
    
    await callback.message.answer(
        f"Ви вибрали жанр: {genre}"
    )