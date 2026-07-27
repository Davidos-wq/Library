from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column,relationship
from sqlalchemy import text,select
from sqlalchemy import ForeignKey,DateTime,Index,BigInteger
from typing import List
from database import Base,engine,async_session_factroy
from datetime import datetime,timedelta
import json

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

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[int]
    genre: Mapped[str]
    borowed_connection: Mapped[List["BorrowedBook"]] = relationship(back_populates="book_info")

    __table_args__ = (
        Index(
            "ix_title_trgm",
            "title",
            postgresql_using="gin",
            postgresql_ops={"title": "gin_trgm_ops"}
        ),
    )


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id:Mapped[int] = mapped_column(primary_key = True)
    user_id:Mapped[int] = mapped_column(BigInteger,ForeignKey("users.tg_id"))
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
    
async def init_db():
    async with async_session_factroy() as session:
        result = await session.execute(select(Book).limit(1)) # Пошук книжок
        if result.scalar_one_or_none() is None:
           
           with open('my_books.json','r',encoding='utf-8') as file:
               books = json.load(file)

           for genre, books_list in books.items():
                for book in books_list:
                    new_book = Book(
                        title=book.get("title"),
                        author=book.get("author"),
                        year=book.get("year"),
                        genre=book.get("genre"))
                    session.add(new_book)
        await session.commit()  

