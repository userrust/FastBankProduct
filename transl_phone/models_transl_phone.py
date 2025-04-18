from pydantic import BaseModel, field_validator
from fastapi import HTTPException, status


class TranslatePhoneSchema(BaseModel):
    user_id: str
    number_phone: str
    summa: str
    comment: str

    @field_validator("number_phone")
    def validator_number_phone(cls, value):
        if len(value) != 12 or value[0] != "+" or value[1] != "7":
            print("12334")
            raise ValueError("Некоректный номер телефона")
        return value
