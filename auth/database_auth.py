from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, Column, Integer, String, Float

engine = create_async_engine(
    r"sqlite+aiosqlite:///D:\Пользователи\Андрюша\Програмирование\FastBank\FastBanck/FastBank.db"
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


class SecreteCode(Base):
    __tablename__ = "secrete_code"
    id = Column(Integer, primary_key=True)
    user_number_phone = Column(String)
    user_secrete_code = Column(String)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def auth_user(number_phone: str):
    async with session_database() as session:
        select_in_users = await session.execute(select(Users).where(Users.number_phone == number_phone))
        res = select_in_users.scalar()

        if res:
            print(res.chat_id)
            return res.chat_id

        return None


async def add_code(number_phone: str, secrete_code: str):
    async with session_database() as session:
        code_select = SecreteCode(user_number_phone=number_phone, user_secrete_code=secrete_code)
        session.add(code_select)

        await session.commit()


async def examination_secrete_code(number_phone: str, secrete_code: str):
    async with session_database() as session:
        exam_code = await session.execute(
            select(SecreteCode).where(SecreteCode.user_secrete_code == secrete_code).where(
                SecreteCode.user_number_phone == number_phone))
        result = exam_code.scalar()

        if result:
            return True


async def search_user_id(number_phone: str):
    async with session_database() as session:
        search = await session.execute(select(Users).where(Users.number_phone == number_phone))
        result = search.scalar()

        return result.id
