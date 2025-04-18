from pydantic import BaseModel, field_validator
from fastapi import HTTPException, status


class TranslateCardSchema(BaseModel):
    user_id: int
    data_card: str
    money: int
    comment: str

    @field_validator("data_card")
    def validate_data_card(cls, value):
        if len(value) != 16:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Введен некоректный номер карты, пожалуйста проверьте номер карты и повторите попытку.")
        return value