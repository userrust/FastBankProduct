from fastapi import APIRouter
from .models_data_chet import DataChetSchema
from .database_data_chet import init_db, information_chet_user

data_chet = APIRouter()


@data_chet.post("/data_chet_user")
async def data_chet_user(data: DataChetSchema):
    await init_db()
    info_user_chet = str(await information_chet_user(data.user_id))

    res_info = [info_user_chet.replace("(", "").replace(")", "").replace(",", "")]
    print(res_info)
    return res_info
