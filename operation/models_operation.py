from pydantic import BaseModel


class OperationSchema(BaseModel):
    user_ids: int