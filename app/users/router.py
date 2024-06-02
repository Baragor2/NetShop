from fastapi import APIRouter, Depends, status

from app.config import auth_jwt
from app.users.auth import hash_password, check_exists, create_access_token, create_refresh_token
from app.users.dao import UsersDAO
from app.users.dependencies import authenticate_user, get_current_user, http_bearer, get_current_user_by_refresh
from app.users.schemas import SLoginUser, SRegisterUser, Token, SUsers, SMeUser

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"],
    dependencies=[Depends(http_bearer)]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: SRegisterUser) -> dict:
    await check_exists(user_data)

    hashed_password = hash_password(user_data.password)
    await UsersDAO.add(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        active=True,
        role="user",
    )
    return {"message": "successful registration"}


@router.post("/login", response_model=Token)
async def login_user(user: SLoginUser = Depends(authenticate_user)):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/me")
async def read_users_me(current_user: SMeUser = Depends(get_current_user)) -> SMeUser:
    return current_user


@router.post(
    "/refresh",
    response_model=Token,
    response_model_exclude_none=True,
)
async def get_new_access_token(
    user: SLoginUser = Depends(get_current_user_by_refresh)
):
    access_token = create_access_token(user)
    return Token(
        access_token=access_token,
    )
