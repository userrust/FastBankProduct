from pydantic import BaseModel


class UserChatModels(BaseModel):
    user_id: int
    text: str


class InfoChat(BaseModel):
    user_id: int
