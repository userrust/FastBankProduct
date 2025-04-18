from sqlalchemy import String, Integer, Column, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import asyncio

engine = create_async_engine(
    r"sqlite+aiosqlite:///D:/Пользователи/Андрюша/Програмирование/FastBank/FastBanck/FastBank.db"
)

session_database = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Operation(Base):
    __tablename__ = "operation"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    operation = Column(String)
    data_time = Column(String)


async def init_db():
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)


async def operation_user_info(user_id: int):
    async with session_database() as session:
        operation = await session.execute(
            select(Operation.operation, Operation.data_time).where(Operation.user_id == user_id))
        res_operation = operation.all()

        if res_operation:
            return res_operation
        else:
            return "Операций пока нет"
