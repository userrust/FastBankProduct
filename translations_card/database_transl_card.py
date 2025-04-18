from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import select
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, String, Column, Integer, Float
from fastapi import HTTPException, status

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


async def info_translate_card(user_id: int, data_card: str, money: int):
    async with session_database() as session:
        examination_user = await session.execute(select(Users).where(Users.data_chet == data_card))
        result_examination_user = examination_user.scalar()

        if not result_examination_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователя с таким номером счета не существует")

        if result_examination_user.id == user_id:
            return "Вы не можете переводить деньги сами себе"

        try:
            payee_card = await session.execute(select(Users).where(Users.data_chet == data_card))
            res_payee = payee_card.scalar()  # Находим пользователя (Получатель платежа) по номеру карты

            payment_sender_user = await session.execute(select(Users).where(Users.id == user_id))
            res_payment_sender = payment_sender_user.scalar()  # Находим пользователя (Отпровителя платежа) по id

            if res_payment_sender.val_chet_one < money:
                return "На вашей карте недостаточно средств"

            res_payee.val_chet_one += money
            res_payment_sender.val_chet_one -= money

            session.add(res_payee)
            session.add(res_payment_sender)

            await session.commit()

            time_now = str(datetime.now())
            res = time_now[0: 19]

            await new_operation_user_payment_sender(res_payment_sender.id, f"-{money}", res)
            await new_operation_user_payee(res_payee.id, f"+{money}", res)
            print("CHAT_ID", res_payment_sender.chat_id)
            arr = [
                res_payment_sender.chat_id,
                res_payment_sender.name,
                res_payment_sender.sur_name,
                res_payment_sender.val_chet_one,

                res_payee.chat_id,
                res_payee.name,
                res_payee.sur_name,
                res_payee.val_chet_one
            ]

            return arr

        except Exception as error:
            print(error)

            return "Произошла ошибка попробуйте поже"
