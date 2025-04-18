from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from .ai_message import ai_generate
from .database_chat import add_info_ai, add_info_user, init_db, information_user_message
from fastapi.middleware.cors import CORSMiddleware


class UserChatModels(BaseModel):
    user_id: int
    text: str


class InfoChat(BaseModel):
    user_id: int


chat = APIRouter()


@chat.post("/info_chat")
async def info_chat_user(data: InfoChat):
    await init_db()

    info_chat = await information_user_message(data.user_id)

    return info_chat


@chat.post("/user_info_chat")
async def hello(data: UserChatModels):
    try:

        await init_db()

        await add_info_user(data.user_id, data.text)
        message = await ai_generate(data.text)

        await add_info_ai(data.user_id, data.text, message)
        print(message)
        return message
    except Exception as e:
        print(e)
