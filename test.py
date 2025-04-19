from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, String, Column, Integer, Float
import os
from pathlib import Path
import asyncio

'''
# Получаем абсолютный путь к директории с базой данных
DB_PATH = Path(__file__).parent / "FastBank.db"

engine = create_async_engine(
    f"sqlite+aiosqlite:///{DB_PATH}"
)'''

engine = create_async_engine(
    f"sqlite+aiosqlite:///FastBank.db"
)

session_database = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sur_name = Column(String)
    middle_name = Column(String)
    number_phone = Column(String)
    chet_one = Column(String)
    chet_two = Column(String)
    chet_three = Column(String)
    val_chet_one = Column(Float)
    val_chet_two = Column(Float)
    val_chet_three = Column(Float)
    data_chet = Column(String)
    chat_id = Column(String)


async def init_db():
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)


async def info():
    async with session_database() as session:
        search_user_id = await session.execute(select(Users).where(Users.id == 1))
        result_search_user_id = search_user_id.scalar()

        return result_search_user_id.chet_two


asyncio.run(init_db())

a = asyncio.run(info())
print(a)
