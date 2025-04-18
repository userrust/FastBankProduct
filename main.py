import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, status, Form
from models import ExaminationSchema, HomeSchema, UserID
from database import info_user_for_home, init_db, info_user_for_home_user_id, save_photo_user, search_user_id
from operation.operation import operation
from data_chet.data_chet import data_chet
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from register import app_reg
import os
from fastapi.staticfiles import StaticFiles
from parser.parser import get_currency_rate
from auth.auth import auth_router
from chat.chat import chat
from transl_phone.translations_phone import app_phone
from translations_card.translations_card import translations_card
from new_chet.new_chet import apps
from telegram_bot.register_bot import main_tg
import asyncio

# Папка для загрузки изображений (создайте её вручную)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app = FastAPI()

phone = ['']

app.include_router(operation, prefix="/operation")
app.include_router(data_chet, prefix="/data_chet")
app.include_router(data_chet, prefix="/data_chet")
app.include_router(chat, prefix="/chat")
app.include_router(app_reg, prefix="/app_reg")
app.include_router(auth_router, prefix="/v")
app.include_router(translations_card, prefix="/translations_card")
app.include_router(app_phone, prefix="/app_phone")
app.include_router(apps, prefix="/apps")

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # При деплои изменить!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/user_auth_number")
async def user_auth(data: HomeSchema):
    print(data)
    if data.number_phone:
        phone[0] = data.number_phone
        print("phone: ", phone)
        return "OK"


@app.post("/user_in_app")
async def user_in_app(data: ExaminationSchema):
    await init_db()
    print(data)
    if data:
        info = await info_user_for_home(phone[0])

        if info:
            return info


@app.post("/user_in_app_po_user_id")
async def user_in_app(data: UserID):
    await init_db()
    print(data)
    if data:
        info = await info_user_for_home_user_id(data.user_id)

        print(info)
        if info:
            return info


import uuid


@app.post("/upload")
async def upload_photo(photo: UploadFile = File(...), user_id: str = Form(...)):
    await init_db()
    try:
        print(user_id)
        # Проверка что это изображение
        if not photo.content_type.startswith("image/"):
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Только изображения разрешены")
        er = await search_user_id(int(user_id))

        p = "uploads/"
        res = p + f"{er[0]}"
        if er:
            os.remove(res)

        # Генерируем уникальное имя файла
        file_ext = photo.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Сохраняем файл
        with open(file_path, "wb") as buffer:
            buffer.write(await photo.read())
        await save_photo_user(int(user_id), filename)

        return {"name_photo":filename}
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка. Попробуйте поже")


@app.get("/home")
async def home():
    return FileResponse("akaunt.html")


@app.get("/eshe")
async def eshe():
    return FileResponse("eshe.html")


@app.get("/")
async def h():
    return FileResponse("test.html")


@app.get("/auth")
async def h():
    return FileResponse("auth.html")


@app.get("/chat")
async def h():
    return FileResponse("chat.html")


@app.get("/exam")
async def auth():
    return FileResponse("exam_telegram_code.html")


@app.get("/curs_usd")
async def curs():
    usd = get_currency_rate('USD')
    eur = get_currency_rate('EUR')
    cny = get_currency_rate('CNY')
    print(usd)
    print(eur)
    print(cny)
    return {
        "usd":usd,
        "eur":eur,
        "chy":cny
    }


# В самом конце файла замените блок if __name__ == "__main__" на это:
if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT",
                              8000))  # Получаем порт из переменной окружения или используем 8000 для локального запуска

    asyncio.run(main_tg())

    # Запускаем FastAPI
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)  # На Render reload должен быть False