from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, String, Column, Integer
import os

# Настройки подключения к PostgreSQL (лучше вынести в переменные окружения)
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "eU2NDKOVu8cHT3Ke61tLWITQ7CTzz0IG")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "dpg-d01lln3e5dus73bau910-a")  # только хост
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "fastbankpost")

# Строка подключения для PostgreSQL
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Создаем асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=True  # Логирование SQL-запросов (для отладки)
)

# Создаем фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


class Text(Base):
    __tablename__ = "texts"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)


# Инициализация БД
async def init_db():
    """Инициализация базы данных (создание таблиц)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Создание нового текста
async def create_text(text: str):
    async with AsyncSessionLocal() as session:
        new_text = Text(text=text)
        session.add(new_text)
        await session.commit()
        await session.refresh(new_text)
        return new_text
