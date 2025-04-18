from pydantic import BaseModel, field_validator
from fastapi import HTTPException, status


class BaseU(BaseModel):
    name: str
    sur_name: str
    middle_name: str
    number_phone: str
    secrete_key_session: str

    @field_validator("name")
    def validator_name(cls, value):
        if len(value) < 2 or len(value) > 12:
            raise ValueError("Длина имени от 2 до 12 символов")
        return value

    @field_validator("sur_name")
    def validator_sur_name(cls, value):
        if len(value) < 4 or len(value) > 20:
            raise ValueError("Длина фамилие от 4 до 20 символов")
        return value

    @field_validator("middle_name")
    def validator_middle_name(cls, value):
        if len(value) < 4 or len(value) > 20:
            raise ValueError("Длина отчества от 4 до 20 символов")
        return value

    @field_validator("number_phone")
    def validator_number_phone(cls, value):
        if len(value) != 12:
            raise ValueError("Некоректный номер телефона")
        return value


class Info(BaseModel):
    secrete_key_session: str
    chat_id: str
