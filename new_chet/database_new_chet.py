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
    chat_id = Column(String)


async def init_db():
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)


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

async def translations_chet_user(user_id: int, money: int, name_chet_payee: str, name_chet_payment: str):
    async with session_database() as session:
        search = await session.execute(select(Users).where(Users.id == user_id))
        res = search.scalar()

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
