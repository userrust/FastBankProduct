from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, select, Float
import random

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


async def add_info(name, sur_name, number_phone, middle_name, data_chet, chat_id):
    async with session_database() as session:
        examination_chet = await session.execute(select(Users.data_chet).where(Users.data_chet == data_chet))
        result_examination_chet = examination_chet.first()

        examination_phone = await session.execute(select(Users.number_phone).where(Users.number_phone == number_phone))
        result_examination_phone = examination_phone.first()

        if result_examination_phone:
            return "Данный номер телефона уже зарегистрирован"

        if not result_examination_chet:
            new_user = Users(name=name, sur_name=sur_name, middle_name=middle_name, number_phone=number_phone,

                             chet_one="Главный щет", chet_two="not",

                             chet_three="not", val_chet_one=100, val_chet_two=0, val_chet_three=0,

                             data_chet=data_chet, chat_id=chat_id)
            session.add(new_user)
            await session.commit()
        else:
            print("Сщета сошлись")
            random_chet = random.randint(234199141973, 935131771973)
            new_user = Users(name=name, sur_name=sur_name, middle_name=middle_name, number_phone=number_phone,

                             chet_one="Главный щет", chet_two="not",

                             chet_three="not", val_chet_one=100, val_chet_two=0, val_chet_three=0,

                             data_chet=f"5533{random_chet}", chat_id=chat_id)
            session.add(new_user)
            await session.commit()


class RegisterBot(Base):
    __tablename__ = "registerBot"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sur_name = Column(String)
    middle_name = Column(String)
    number_phone = Column(String)
    secrete_key_session = Column(String)


async def add(name: str, sur_name: str, middle_name: str, number_phone: str, secrete_key_session: str):
    async with session_database() as session:
        new_info = RegisterBot(name=name, sur_name=sur_name, middle_name=middle_name, number_phone=number_phone,
                               secrete_key_session=secrete_key_session)
        session.add(new_info)
        await session.commit()


async def poisk_data(secrete_key_session: str):
    async with session_database() as session:
        poisk = await session.execute(select(RegisterBot).where(RegisterBot.secrete_key_session == secrete_key_session))
        result_data = poisk.scalar()

        if not result_data:
            return False

        print(result_data.name)
        return result_data.name, result_data.sur_name, result_data.middle_name, result_data.number_phone


async def exam_user_chat_id(chat_id: str):
    async with session_database() as session:
        examination = await session.execute(select(Users).where(Users.chat_id == chat_id))
        result_examination = examination.first()

        if not result_examination:
            return True


async def exam_user_number_phone(number_phone: str):
    async with session_database() as session:
        examination = await session.execute(select(Users).where(Users.number_phone == number_phone))
        result_examination = examination.scalar()

        if result_examination:
            print("YESSS")
            return True
        else:
            print("NO")
