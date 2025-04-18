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
    chat_id = Column(String)


class UserMessage(Base):
    __tablename__ = "UserMessage"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    text_user = Column(String)


class AIMessage(Base):
    __tablename__ = "AIMessage"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    text_user = Column(String)
    text_ai = Column(String)


async def init_db():
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)


async def add_info_user(user_id: int, text: str):
    async with session_database() as session:
        new = UserMessage(user_id=user_id, text_user=text)

        session.add(new)
        await session.commit()


async def add_info_ai(user_id: int, text_user: str, text_ai):
    async with session_database() as session:
        new = AIMessage(user_id=user_id, text_user=text_user, text_ai=text_ai)

        session.add(new)
        await session.commit()


async def information_user_message(user_id):
    async with session_database() as session:
        search_user = await session.execute(select(UserMessage).where(UserMessage.user_id == user_id))
        res_user = search_user.scalars().all()

        search_ai = await session.execute(select(AIMessage).where(AIMessage.user_id == user_id))
        res_ai = search_ai.scalars().all()

        chat = []

        for result_user, result_ai in zip(res_user, res_ai):
            chat.append(result_user.text_user)
            chat.append(result_ai.text_ai)

        print(chat)
        return chat