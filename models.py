from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column,relationship
from sqlalchemy import ForeignKey,DateTime
from typing import List
from database import Base,engine
from datetime import datetime,timedelta

class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True)
    tg_id:Mapped[int]
    name:Mapped[str]
    lastname:Mapped[str]
    loved_genre:Mapped[str]
    user_books:Mapped[List["BorrowedBook"]] = relationship(back_populates="bought_book")


class Book(Base):
    __tablename__ = "books"

    id:Mapped[int] = mapped_column(primary_key = True)
    title:Mapped[str]
    author:Mapped[str]
    year:Mapped[int]
    genre:Mapped[str]
    borowed_connection:Mapped[List["BorrowedBook"]] = relationship(back_populates="book_info")


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id:Mapped[int] = mapped_column(primary_key = True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id:Mapped[int] = mapped_column(ForeignKey("books.id"))
    
    time_bought: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now()
    )

    time_end: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now() + timedelta(days=14)
    )

    book_info:Mapped["Book"] = relationship(back_populates="borowed_connection")
    bought_book:Mapped["User"] = relationship(back_populates="user_books")

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

