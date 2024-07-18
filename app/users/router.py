from fastapi import APIRouter, Depends, status

from app.users.auth import hash_password, check_exists, create_access_token, create_refresh_token
from app.users.dao import UsersDAO
from app.users.dependencies import authenticate_user, get_current_user, http_bearer, get_current_user_by_refresh, \
    check_admin_role
from app.users.schemas import SLoginUser, SRegisterUser, Token, SMeUser, Username

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"],
    dependencies=[Depends(http_bearer)]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: SRegisterUser) -> dict:
    await check_exists(user_data)

    hashed_password: bytes = hash_password(user_data.password)

    await UsersDAO.add_user_and_cart(user_data, hashed_password)

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
) -> Token:
    access_token = create_access_token(user)
    return Token(
        access_token=access_token,
    )


@router.patch("/ban/{username}")
async def ban_user(
        username: Username,
        current_user: SMeUser = Depends(get_current_user)
) -> dict[str, str]:
    await check_admin_role(current_user.name)

    await UsersDAO.deactivate_user(username)
    return {"message": "successful ban operation"}
