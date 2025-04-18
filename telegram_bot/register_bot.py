from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import httpx
from database_register import init_db, exam_user_chat_id

API_TOKEN = '7813157064:AAFxB7O2oxbxCNY8RTEgaVpdP0GH_H0b7Bs'  # Замените на токен вашего бота

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

headers = {
    "Accept":"application/json",
    "Content-Type":"application/json"
}

url = "https://hellohost-8hql.onrender.com/app_reg/info"


async def req(secrete_key_session, chat_id):
    data = {
        "secrete_key_session":f"{secrete_key_session}",
        "chat_id":f"{chat_id}"
    }
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url=url, headers=headers, json=data)
        except Exception as e:
            print(e)


@dp.message(Command("start"))
async def send_welcome(message: types.Message, command: Command):
    await message.answer("Добро пожаловать в FastBank! Этот бот необходим для подтверждения данных при регистрации.")
    secrete_key_session = command.args
    chat_id = message.chat.id

    await init_db()

    q = await exam_user_chat_id(str(chat_id))
    print("1", secrete_key_session, chat_id)
    if q:
        print("2", secrete_key_session, chat_id)
        await req(secrete_key_session, chat_id)
        await message.answer(
            "Данные подтверждены! Поздравляем, вы зарегистрировались в FastBank. Для входа в аккаунт вернитесь на сайт и нажмите на вкладку «Личный кабинет». ")
    else:
        print("Пользователь уже существует")
        await message.answer("Вы не можете создать второй аккаунт")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
