from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, String, Column, Integer, Float
import os
from pathlib import Path

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


class RegisterBot(Base):
    __tablename__ = "registerBot"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sur_name = Column(String)
    middle_name = Column(String)
    number_phone = Column(String)
    secrete_key_session = Column(String)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


import sqlite3


def test():
    con = sqlite3.connect("FastBank.db")
    cur = con.cursor()

    cur.execute("INSERT INTO registerBot(name, sur_name, middle_name, number_phone, number_phone) VALUES (?, ?, ?, ?, ?)",
                ("1", "1", "1", "1", "1"))
    con.commit()
    con.close()

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
        try:
            # Проверка входных данных
            if not new_name_chet or not isinstance(new_name_chet, str):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Новое имя счета должно быть непустой строкой"
                )

            # Поиск пользователя
            result = await session.execute(
                select(Users)
                .where(Users.id == user_id)
                .with_for_update()  # Блокировка строки для изменения
            )
            user = result.scalar()

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Пользователь с ID {user_id} не найден"
                )

            # Проверка и обновление
            updated = False
            if user.chet_one == past_name_chet:
                user.chet_one = new_name_chet
                updated = True
            elif user.chet_two == past_name_chet:
                user.chet_two = new_name_chet
                updated = True
            elif user.chet_three == past_name_chet:
                user.chet_three = new_name_chet
                updated = True

            if not updated:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Счет с именем '{past_name_chet}' не найден"
                )

            # Не требуется явный add() для существующего объекта
            await session.commit()

            # Обновляем объект в сессии
            await session.refresh(user)

            return {
                "status":"success",
                "message":"Имя счета успешно изменено",
                "new_name":new_name_chet
            }

        except HTTPException:
            raise  # Перебрасываем уже обработанные ошибки
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при переименовании счета: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Внутренняя ошибка сервера: {str(e)}"
            )


async def info():
    async with session_database() as session:
        search_user_id = await session.execute(select(Users).where(Users.id == 1))
        result_search_user_id = search_user_id.scalar()

        return result_search_user_id.chet_two


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


async def translations_chet_user(user_id: int, money: int, name_chet_payee: str, name_chet_payment: str):
    async with session_database() as session:
        print(user_id)
        search = await session.execute(select(Users).where(Users.id == user_id))
        res = search.scalar()
        print(res)
        chet_one = res.chet_one
        chet_two = res.chet_two
        chet_three = res.chet_three
        chat_id = res.chat_id
        balance = res.val_chet_one
        print(chet_one, name_chet_payment)
        try:
            if chet_one == name_chet_payment and chet_two == name_chet_payee:
                if res.val_chet_one < money:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="На счете недостатосно средств")
                res.val_chet_one -= money
                res.val_chet_two += money
                await session.commit()
                return [chat_id, balance]
            elif chet_one == name_chet_payment and chet_three == name_chet_payee:
                if res.val_chet_one < money:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="На счете недостатосно средств")
                res.val_chet_one -= money
                res.val_chet_three += money
                await session.commit()
                return [chat_id, balance]
            if chet_two == name_chet_payment and chet_one == name_chet_payee:
                if res.val_chet_two < money:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="На счете недостатосно средств")
                res.val_chet_two -= money
                res.val_chet_one += money
                await session.commit()
                return [chat_id, balance]
            elif chet_two == name_chet_payment and chet_three == name_chet_payee:
                if res.val_chet_two < money:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="На счете недостатосно средств")
                res.val_chet_two -= money
                res.val_chet_three += money
                await session.commit()
                return [chat_id, balance]

            if chet_three == name_chet_payment and chet_two == name_chet_payee:
                if res.val_chet_three < money:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="На счете недостатосно средств")
                res.val_chet_three -= money
                res.val_chet_two += money
                await session.commit()
                return [chat_id, balance]
            elif chet_three == name_chet_payment and chet_one == name_chet_payee:
                if res.val_chet_three < money:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="На счете недостатосно средств")
                res.val_chet_three -= money
                res.val_chet_one += money
                await session.commit()
                return [chat_id, balance]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
