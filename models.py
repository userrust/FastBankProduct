from pydantic import BaseModel, field_validator


class HomeSchema(BaseModel):
    number_phone: str


class ExaminationSchema(BaseModel):
    secret_activation: str


class UserID(BaseModel):
    user_id: int


class PhotoUser(BaseModel):
    user_id: int
    photo: str
