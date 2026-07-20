# from aiogram.types import InlineKet
from aiogram.utils.keyboard import InlineKeyboardBuilder


#Розкладка вибору жанру
def get_my_keyboard():
   builder = InlineKeyboardBuilder()

   builder.button(text="Фантастика",callback_data="Science Fiction")
   builder.button(text="Фенезі",callback_data="Fantasy")
   builder.button(text="Детектив",callback_data="Mystery")
   builder.button(text="Романтика",callback_data="Romance")
   builder.button(text="Жахи",callback_data="Horror")
   builder.button(text="Сучасна класика",callback_data="Literary Fiction")

   
   return builder.as_markup()

