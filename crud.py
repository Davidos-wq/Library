from sqlalchemy import select,delete,func
from sqlalchemy import or_
from sqlalchemy.orm import joinedload,selectinload,with_loader_criteria
from models import Book,User,BorowedBook
from sqlalchemy.exc import NoResultFound
from datetime import datetime
import time


async def add_info(session,user_id,
                   username,lastname,genre):
    
    user = select(User).where(User.tg_id==user_id)
    if user:
        user.tg_id = user_id
        user.name = username
        user.lastname = lastname
        user.loved_genre = genre
    
    else:
        user = User(tg_id=user_id,name=username,
                    lastname=lastname,genre=genre)
        
        session.add(user)  
    await session.commit()