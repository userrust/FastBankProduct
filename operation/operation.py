from fastapi import APIRouter
from .database_operation import init_db, operation_user_info
from .models_operation import OperationSchema

operation = APIRouter()


@operation.post("/operation")
async def operation_user(data: OperationSchema):
    await init_db()

    result_operations = await (operation_user_info(str(data.user_ids)))
    sting_result = str(result_operations)

    validation_string = [sting_result.replace("(", "").replace(")", "")]
    result_validation = str(validation_string)

    res = result_validation[3: -3]

    return res
