from fastapi import HTTPException, status, FastAPI, APIRouter
from .models_transl_phone import TranslatePhoneSchema
from .database_transl_phone import info_translate_phone, init_db
from .message_user import send_message_user

app_phone = APIRouter()


@app_phone.post("/translations_phone", status_code=status.HTTP_200_OK)
async def translations_phone_money(data: TranslatePhoneSchema):
    await init_db()
    print(data)
    user_id = int(data.user_id)
    money = int(data.summa)

    try:

        transl = await info_translate_phone(user_id, data.number_phone, money)
        print(transl, transl[0])

        sur_name_payee = str(transl[5])
        r = list(sur_name_payee)
        comment = ""
        res_comment = ""
        if data.comment:
            comment = ".Коментарий: ", data.comment
            res_comment = comment[2: len(comment) - 2]

        if data.comment:
            comment_user = f"Коментарий: {data.comment}."
            res_comment = comment_user

        sender = send_message_user(transl[0],
                                   f"Перевод на {data.summa}₽, счет RUB. {transl[6]} {r[0]}. Баланс {transl[3]}₽")
        payee = send_message_user(transl[4],
                                  f"Пополнение на {data.summa}₽, счет RUB. {transl[2]} {r[0]} Доступно {transl[7]}₽. {res_comment}")

        return {"message":"Перевод успешно выполнен"}
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
