from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, String, Column, Integer, Float
from pydantic import BaseModel
from fastapi import FastAPI
import os

app = FastAPI()

# Настройки подключения к PostgreSQL (лучше вынести в переменные окружения)
POSTGRES_USER = os.getenv("fastbankpost_user", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "eU2NDKOVu8cHT3Ke61tLWITQ7CTzz0IG")
POSTGRES_HOST = os.getenv("POSTGRES_HOST",
                          "postgresql://fastbankpost_user:eU2NDKOVu8cHT3Ke61tLWITQ7CTzz0IG@dpg-d01lln3e5dus73bau910-a/fastbankpost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "fastbankpost_user")

# Строка подключения для PostgreSQL
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Создаем асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=True  # Логирование SQL-запросов (для отладки)
)

# Создаем фабрику сессий
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Text(Base):
    __tablename__ = "texts"
    id = Column(Integer, primary_key=True)
    text = Column(String)


async def init_db():
    """Инициализация базы данных (создание таблиц)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_text(text: str) -> Text:
    """Создание новой записи в БД"""
    async with AsyncSessionLocal() as session:
        new_text = Text(text=text)
        session.add(new_text)
        await session.commit()
        await session.refresh(new_text)
        return new_text
