from fastapi import APIRouter, Body, HTTPException, status
from .database_new_chet import init_db, examination_chet, rename_name_chet, delete_chet_user, translations_chet_user
from .models_new_chet import NewChetSchema, RenameSchema, DeleteChetSchema, TranslationChetUser
from .message_user import send_message_user
import uvicorn

apps = APIRouter()


@apps.post("/new_chet")
async def new_chet_user(data: NewChetSchema):
    await init_db()
    print(data.user_id)
    zap = await examination_chet(str(data.user_id), data.name_chet)
    print(zap)
    return zap


@apps.post("/rename_chet")
async def rename_chet(data: RenameSchema):
    print(data)
    await init_db()
    await rename_name_chet(data.user_id, data.past_chet_name, data.new_name_chet)
    return True


@apps.post("/delete_chet")
async def delete_chet(data: DeleteChetSchema):
    await init_db()
    print(data)
    await delete_chet_user(data.user_id, data.name_delete_chet)
    return True


@apps.post("/translations_chet")
async def translations_chet(data: TranslationChetUser):
    print(data)
    try:
        await init_db()
        tr = await translations_chet_user(int(data.user_id), int(data.money), data.name_chet_two, data.name_chet_one)

        send_message_user(tr[0], f"Перевод на {data.money} ₽, счет RUB. Баланс {tr[1]} ₽")

        return {"message":"Перевод успешно выполнен"}
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
