from pydantic import BaseModel


class DataChetSchema(BaseModel):
    user_id: int
