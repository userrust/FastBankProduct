from pydantic import BaseModel, field_validator
from fastapi import HTTPException, status


class AuthSchema(BaseModel):
    number_phone: str

    @field_validator("number_phone")
    def validator_number_phone(cls, value):
        if len(value) != 12:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некоректный номер телефона")
        return value


class SecreteCodeSchema(BaseModel):
    number_phone: str
    code: str
