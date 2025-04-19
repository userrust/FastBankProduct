from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, delete
from sqlalchemy import Column, Integer, String, Float
import asyncio

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


class PhotoUser(Base):
    __tablename__ = "photo_user_logo"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name_photo = Column(String)


async def init_db():
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)


from fastapi import HTTPException


async def info_user_for_home(number_phone: str):
    async with session_database() as session:
        # Ищем пользователя
        select_in_users = await session.execute(
            select(Users).where(Users.number_phone == number_phone)
        )
        user = select_in_users.scalar()

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="Пользователь с таким номером телефона не найден"
            )

        # Получаем все операции пользователя
        transl_user = await session.execute(
            select(Operation).where(Operation.user_id == user.id)
        )
        operations = transl_user.scalars().all()

        # Возвращаем данные пользователя
        return {
            "info":{
                "user_id":user.id,
                "info_carta":user.data_chet,
                "name":user.name,
                "sur_name":user.sur_name,
                "middle_name":user.middle_name,
                "chet_one":user.chet_one,
                "chet_two":user.chet_two,
                "chet_three":user.chet_three,
                "val_chet_one":user.val_chet_one,
                "val_chet_two":user.val_chet_two,
                "val_chet_three":user.val_chet_three
            },

            "operation_user":[
                {
                    "data_operation":i.data_time,
                    "summa_operation":i.operation,

                }
                for i in operations
            ]
        }


async def info_user_for_home_user_id(user_id: int):
    async with session_database() as session:
        # Ищем пользователя
        select_in_users = await session.execute(
            select(Users).where(Users.id == user_id)
        )
        user = select_in_users.scalar()

        # Получаем все операции пользователя
        transl_user = await session.execute(
            select(Operation).where(Operation.user_id == user.id)
        )
        operations = transl_user.scalars().all()

        # Возвращаем данные пользователя
        return {
            "info":{
                "user_id":user.id,
                "info_carta":user.data_chet,
                "name":user.name,
                "sur_name":user.sur_name,
                "middle_name":user.middle_name,
                "number_phone":user.number_phone,
                "chet_one":user.chet_one,
                "chet_two":user.chet_two,
                "chet_three":user.chet_three,
                "val_chet_one":user.val_chet_one,
                "val_chet_two":user.val_chet_two,
                "val_chet_three":user.val_chet_three
            },

            "operation_user":[
                {
                    "data_operation":i.data_time,
                    "summa_operation":i.operation,

                }
                for i in operations
            ]
        }


async def save_photo_user(user_id: int, photo: str):
    async with session_database() as session:
        new_check = PhotoUser(user_id=user_id, name_photo=photo)

        session.add(new_check)
        await session.commit()


async def search_user_id(user_id: int):
    async with session_database() as session:
        result = await session.execute(select(PhotoUser).where(PhotoUser.user_id == user_id))
        photos = result.scalars().all()

        photo_names = [photo.name_photo for photo in photos]

        for photo in photos:
            await session.delete(photo)
        await session.commit()

        if photos:
            return photo_names


async def user_info():
    async with session_database() as session:
        info = await session.execute(select(Users.id))
        res = info.scalars().all()

        arr = []

        for i in res:
            arr.append(i)
        print(max(arr))
        return max(arr)
