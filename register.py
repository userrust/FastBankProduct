import random
from fastapi import APIRouter
from fastapi import HTTPException, status
from telegram_bot.database_register import add, add_info, init_db, poisk_data
from telegram_bot.models_register import BaseU, Info

app_reg = APIRouter()


@app_reg.post("/info")
async def new(data: Info):
    await init_db()

    print("data:", data)

    result_data = await poisk_data(data.secrete_key_session)

    if result_data is False:
        print("NO info")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данные не найденны")

    name, sur_name, middle_name, number_phone = result_data
    chat_id = data.chat_id

    data_chet = random.randint(234199141973, 935131771973)

    print(name, sur_name, middle_name, number_phone, chat_id)

    await add_info(name, sur_name, number_phone, middle_name, f"5533{data_chet}", chat_id)
    return "True"


@app_reg.post("/save_prom_info")
async def save_prom_info(data: BaseU):
    print("save_prom_info", data)
    print(data)
    await init_db()
    await add(data.name, data.sur_name, data.middle_name, data.number_phone, data.secrete_key_session)

    return True
