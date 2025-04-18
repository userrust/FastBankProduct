from fastapi import FastAPI, HTTPException, status, APIRouter
from .models_auth import AuthSchema, SecreteCodeSchema
import httpx
from fastapi.responses import FileResponse
from .database_auth import init_db, auth_user, add_code, examination_secrete_code, search_user_id
import random
from .auth_bot import send_telegram_message
from fastapi.middleware.cors import CORSMiddleware

auth_router = APIRouter()

# app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["*"],  # Разрешенные источники
#    allow_credentials=True,
#    allow_methods=["*"],  # Разрешенные методы (GET, POST, etc)
#    allow_headers=["*"],  # Разрешенные заголовки
# )

url = "http://127.0.0.1:8001/user_auth_number"  # URL адрес 2 микросервиса ( HOME )

headers = {
    "Accept":"application/json"
}


async def submit_number(number_phone):
    async with httpx.AsyncClient() as client:
        data = {"number_phone":f"{number_phone}"}
        await client.post(url=url, json=data, headers=headers)


@auth_router.post("/auth_user", status_code=status.HTTP_200_OK)
async def auth(data: AuthSchema):
    print(data)
    await init_db()
    examination_number_phone = await auth_user(data.number_phone)

    if examination_number_phone:
        chat_id = examination_number_phone

        verification_code = str(random.randint(100000, 999999))  # 6-значный код
        await add_code(data.number_phone, verification_code)

        send_telegram_message(chat_id, verification_code)

    return {"message":True}


@auth_router.post("/exam_user", status_code=status.HTTP_200_OK)
async def exam_user_secrete_code(data: SecreteCodeSchema):
    print(data.number_phone, data.code)
    await init_db()

    code = await examination_secrete_code(data.number_phone, data.code)

    if not code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Введен неправильный код")

    user_id = await search_user_id(data.number_phone)

    return {"message": "Вы авторизованы", "user_id": user_id}
