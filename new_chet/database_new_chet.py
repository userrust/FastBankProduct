from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, String, Column, Integer, Float
import os
from pathlib import Path

# Получаем абсолютный путь к директории с базой данных
DB_PATH = Path(__file__).parent / "FastBank.db"

engine = create_async_engine(
    f"sqlite+aiosqlite:///{DB_PATH}"
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
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Таблицы созданы успешно")

        # Проверка наличия тестовых данных
        async with session_database() as session:
            result = await session.execute(select(Users))
            if not result.scalars().first():
                print("Внимание: таблица users пустая!")


async def examination_chet(user_id: str, name_chet: str):
    async with session_database() as session:
        zap = await session.execute(select(Users).where(Users.id == user_id))
        res_select = zap.first()

        user = res_select[0]
        #
        # if user.chet_three not in "not":
        #    return "Достигнуто максимально количестов щетов"

        if user.chet_two in "not":
            if name_chet == "":
                user.chet_two = "Дополнительный щет №1"
            else:
                user.chet_two = name_chet

            user.val_chet_two = "0"
            await session.commit()

        elif user.chet_two not in "not":
            if name_chet == "":
                user.chet_three = "Дополнительный щет №2"
            else:
                user.chet_three = name_chet
            user.val_chet_three = "0"
            await session.commit()

        if res_select is None:
            return "Произошла ошибка попробуйте поже"

        return (
            user.id,
            user.name,
            user.chet_one,
            user.chet_two,
            user.chet_three,
            user.val_chet_one,
            user.val_chet_two,
            user.val_chet_three
        )


async def rename_name_chet(user_id: int, past_name_chet: str, new_name_chet: str):
    async with session_database() as session:
        search_user_id = await session.execute(select(Users).where(Users.id == user_id))
        result_search_user_id = search_user_id.scalar()

        if result_search_user_id.chet_one == past_name_chet:
            result_search_user_id.chet_one = new_name_chet

        elif result_search_user_id.chet_two == past_name_chet:
            result_search_user_id.chet_two = new_name_chet

        elif result_search_user_id.chet_three == past_name_chet:
            result_search_user_id.chet_three = new_name_chet

        session.add(result_search_user_id)
        await session.commit()


async def delete_chet_user(user_id: int, name_chet: str):
    async with session_database() as session:
        search_user_id = await session.execute(select(Users).where(Users.id == user_id))
        result_search_user_id = search_user_id.scalar()

        if result_search_user_id.chet_two == name_chet:
            result_search_user_id.chet_two = "not"
            result_search_user_id.val_chet_one += result_search_user_id.val_chet_two
            result_search_user_id.val_chet_two = 0  # возможно, стоит обнулить

        elif result_search_user_id.chet_three == name_chet:
            result_search_user_id.chet_three = "not"
            result_search_user_id.val_chet_one += result_search_user_id.val_chet_three
            result_search_user_id.val_chet_three = 0  # возможно, стоит обнулить

        session.add(result_search_user_id)
        await session.commit()


from fastapi import HTTPException, status


async def translations_chet_user(user_id: int, money: float, name_chet_payee: str, name_chet_payment: str):
    async with session_database() as session:
        try:
            user = await get_user_or_404(session, user_id)

            # Проверяем валидность суммы
            if money <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Сумма перевода должна быть положительной"
                )

            # Определяем тип перевода
            transfer_cases = {
                (user.chet_one, user.chet_two):(user.val_chet_one, user.val_chet_two),
                (user.chet_one, user.chet_three):(user.val_chet_one, user.val_chet_three),
                (user.chet_two, user.chet_one):(user.val_chet_two, user.val_chet_one),
                (user.chet_two, user.chet_three):(user.val_chet_two, user.val_chet_three),
                (user.chet_three, user.chet_one):(user.val_chet_three, user.val_chet_one),
                (user.chet_three, user.chet_two):(user.val_chet_three, user.val_chet_two),
            }

            source_balance, target_balance = transfer_cases.get(
                (name_chet_payment, name_chet_payee),
                (None, None)
            )

            if source_balance is None or target_balance is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Указанные счета не найдены"
                )

            if source_balance < money:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Недостаточно средств на счете"
                )

            # Выполняем перевод
            source_balance -= money
            target_balance += money

            await session.commit()

            return {
                "chat_id":user.chat_id,
                "balance":user.val_chet_one,
                "message":"Перевод выполнен успешно"
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Ошибка в translations_chet_user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )