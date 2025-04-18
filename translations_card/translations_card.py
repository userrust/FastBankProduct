from fastapi import APIRouter, HTTPException, status, FastAPI
from .models_transl_card import TranslateCardSchema
from .database_transl_card import info_translate_card
from .message_user import send_message_user
from fastapi.middleware.cors import CORSMiddleware

translations_card = APIRouter()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # При деплои изменить!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@translations_card.post("/translations_card", status_code=status.HTTP_200_OK)
async def translations_card_money(data: TranslateCardSchema):
    print(data)

    transl = await info_translate_card(data.user_id, data.data_card, data.money)
    sur_name_payee = str(transl[5])

    r = list(sur_name_payee)

    res_comment = ""
    if data.comment:
        comment = ".Коментарий: ", data.comment
        res_comment = comment[2: len(comment) - 2]

    if data.comment:
        comment_user = f"Коментарий: {data.comment}."
        res_comment = comment_user
    print(transl[0], transl[4])
    q = send_message_user(transl[0], f"Перевод на {data.money}₽, счет RUB. {transl[6]} {r[0]}. Баланс {transl[3]}₽")
    w = send_message_user(transl[4],
                      f"Пополнение на {data.money}₽, счет RUB. {transl[2]} {r[0]} Доступно {transl[7]}₽. {res_comment}")

    return {"message":"Перевод успешно выполнен"}
