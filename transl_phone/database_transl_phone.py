from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import select
from datetime import datetime
import time
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, String, Column, Integer, Float
from fastapi import HTTPException, status

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
    chat_id = Column(String)


class Operation(Base):
    __tablename__ = "operation"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    operation = Column(String)
    data_time = Column(String)


async def init_db():
    async with engine.begin() as conn:  # Используйте conn вместо session
        await conn.run_sync(Base.metadata.create_all)


async def new_operation_user_payment_sender(user_id: int, operation_payment_sender: str, data_time: str):
    async with session_database() as session:
        new_operation_payment_sender = Operation(user_id=user_id, operation=operation_payment_sender,
                                                 data_time=data_time)

        session.add(new_operation_payment_sender)
        await session.commit()


async def new_operation_user_payee(user_id: int, operation_payee: str, data_time: str):
    async with session_database() as session:
        new_operation_payee = Operation(user_id=user_id, operation=operation_payee, data_time=data_time)

        session.add(new_operation_payee)
        await session.commit()


async def info_translate_phone(user_id: int, number_phone: str, money: int):
    async with session_database() as session:

        examination_user = await session.execute(select(Users).where(Users.number_phone == number_phone))
        result_examination_user = examination_user.scalar()

        if not result_examination_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Пользователя с таким номером телефона не существует")

        if result_examination_user.id == user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Вы не можете переводить деньги сами себе")

        try:
            select_id_payment_sender = await session.execute(select(Users).where(Users.id == user_id))
            payment_sender_user = select_id_payment_sender.scalar()  # Отпровитель

            select_phone_payee = await session.execute(select(Users).where(Users.number_phone == number_phone))
            payee_user = select_phone_payee.scalar()  # Получатель

            if payment_sender_user.val_chet_one < money:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="На вашей карте недостаточно средств")

            payee_user.val_chet_one += money
            payment_sender_user.val_chet_one -= money



            await session.commit()
            await session.close()

            time_now = str(datetime.now())
            res = time_now[0: 19]

            await new_operation_user_payment_sender(payment_sender_user.id, f"-{money}", res)
            await new_operation_user_payee(payee_user.id, f"+{money}", res)

            arr = [
                payment_sender_user.chat_id,
                payment_sender_user.name,
                payment_sender_user.sur_name,
                payment_sender_user.val_chet_one,

                payee_user.chat_id, # 4
                payee_user.name, #5
                payee_user.sur_name,#6
                payee_user.val_chet_one#7
            ]

            return arr

        except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
