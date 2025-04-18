from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, String, Column, Integer, Float

engine = create_async_engine(
        r"sqlite+aiosqlite:///FastBank.db"
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


class Operation(Base):
    __tablename__ = "operation"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    operation = Column(String)
    data_time = Column(String)


async def init_db():
    async with engine.begin() as conn:  # Используйте conn вместо session
        await conn.run_sync(Base.metadata.create_all)
