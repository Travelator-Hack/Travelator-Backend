from contextlib import contextmanager

from fastapi import APIRouter, Body, HTTPException, Header

from services import UserService, NewUser


router = APIRouter(prefix="/auth", tags=["User Auth"])


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
