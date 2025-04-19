from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, String, Column, Integer, Float

engine = create_async_engine(
    f"sqlite+aiosqlite:///Test.db"
)

session_database = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Text(Base):
    __tablename__ = "name"
    id = Column(Integer, primary_key=True)
    text = Column(String)


async def init_db2():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def new(text: str):
    async with session_database() as s:
        new = Text(text=text)
        s.add(new)
        await s.commit()
