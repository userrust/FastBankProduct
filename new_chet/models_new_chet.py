from pydantic import BaseModel


class NewChetSchema(BaseModel):
    user_id: str
    name_chet: str


class RenameSchema(BaseModel):
    user_id: int
    new_name_chet: str
    past_chet_name: str


class DeleteChetSchema(BaseModel):
    user_id: int
    name_delete_chet: str


class TranslationChetUser(BaseModel):
    user_id: str
    name_chet_one: str
    name_chet_two: str
    money: str
