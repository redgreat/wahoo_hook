from fastapi import APIRouter
from models.errors import NotFound
from models.user import GetUser
from utils.request import AppRequest

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/get",
    response_model=GetUser,
    responses={200: {"model": GetUser}, 404: {"model": NotFound}},
    name="Get users",
)
async def get_users(request: AppRequest) -> GetUser:
    query = "SELECT 1;"
    await request.app.pool.execute(query)
    return GetUser(user="hi")
