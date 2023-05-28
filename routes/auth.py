from pydantic import BaseModel
from contextlib import contextmanager

from fastapi import APIRouter, Body, HTTPException, Header

from services import UserService, NewUser


router = APIRouter(prefix="/users", tags=["User Auth"])


class UserOut(BaseModel):
    username: str    
    current_city_id: str | None = None
    current_city_name: str | None = None


@contextmanager
def handle_auth_exception():
    """Handle auth related errors and raise fastapi exception."""
    try:
        yield
    except Exception as e:
        raise HTTPException(status_code=403, detail=e.args[0])


@router.post("/token")
async def retrieve_token(data: NewUser = Body(...)):
    with handle_auth_exception():
        return await UserService.authorize(data)


@router.get("/me")
async def get_current_user(token: str = Header(...)):
    with handle_auth_exception():
        return await UserService.verify_token(token)


@router.post("/signup")
async def create_new_user(data: NewUser = Body(...)):
    with handle_auth_exception():
        return await UserService.create(data)


@router.get('/{username}', response_model=UserOut)
async def get_user_data_by_username(username: str):
    with handle_auth_exception():
        return await UserService.single(username, throw=True)
