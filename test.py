import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, String, Column, Integer

DATABASE_URL = "postgresql+asyncpg://fastbankpost_user:eU2NDKOVu8cHT3Ke61tLWITQ7CTzz0IG@dpg-d01lln3e5dus73bau910-a.frankfurt-postgres.render.com:5432/fastbankpost"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)


engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_user(name: str, email: str):
    try:
        async with AsyncSessionLocal() as session:
            new_user = User(name=name, email=email)
            session.add(new_user)
            await session.commit()
            print(f"Добавлен пользователь: {name} ({email})")
    except Exception as e:
        print(f"Ошибка: {e}")


async def add_multiple_users():
    users = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5")
    ]

    for name, email in users:
        await add_user(name, email)


async def count_users() -> int:
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select((User)))
            count = result.scalars().all()

            print(f"Всего пользователей в базе: {count}")
            return count
    except Exception as e:
        print(f"Ошибка при подсчете пользователей: {e}")
        return 0


async def main():
    await init_db()
    await add_multiple_users()  # Добавляем несколько пользователей
    await engine.dispose()  # Закрываем соединение после всех операций
    await count_users()


if __name__ == "__main__":
    asyncio.run(main())
