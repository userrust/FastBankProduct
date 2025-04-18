from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, String, Column, Integer, Float

engine = create_async_engine(
    "sqlite+aiosqlite:///D:\Пользователи\Андрюша\Програмирование\FastBank\FastBanck/FastBank.db")
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

async def init_db():
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)


async def information_chet_user(user_id: int):
    async with session_database() as session:
        data_chet = await session.execute(select(Users.data_chet).where(Users.id == user_id))
        result = data_chet.first()
        print(result)
        return result
