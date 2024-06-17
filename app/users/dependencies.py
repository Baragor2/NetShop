from fastapi import Form, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jwt import InvalidTokenError

from app.config import auth_jwt
from app.exceptions import IncorrectUsernameOrPasswordException, UserIsNotActiveException, InvalidTokenException, \
    NotEnoughRightsException
from app.users.auth import validate_password, decode_jwt
from app.users.dao import UsersDAO
from app.users.schemas import SUser, SLoginUser, SMeUser, Username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
http_bearer = HTTPBearer(auto_error=False)


async def authenticate_user(
        username: Username = Form(),
        password: str = Form(),
) -> SUser:
    user = await get_and_check_user(username)

    if not validate_password(password, user.password):
        raise IncorrectUsernameOrPasswordException

    return user


async def get_and_check_user(
        username: Username,
) -> SUser:
    user: SUser = await UsersDAO.find_one_or_none(name=username)

    if not user:
        raise IncorrectUsernameOrPasswordException

    if not user.active:
        raise UserIsNotActiveException

    return user


async def check_role(
        username: Username,
        is_admin: bool = False,
) -> None:
    user = await UsersDAO.find_one_or_none(name=username)
    if is_admin and user.role != "admin":
        raise NotEnoughRightsException


async def get_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        raise InvalidTokenException

    return payload


def check_token_type(payload: dict, token_type: str) -> None:
    payload_token_type = payload.get(auth_jwt.TOKEN_TYPE_FIELD)
    if payload_token_type != token_type:
        raise InvalidTokenException


async def get_current_user(
    payload: dict = Depends(get_token_payload),
) -> SMeUser:
    check_token_type(payload, auth_jwt.ACCESS_TOKEN_TYPE)

    username: str | None = payload.get("sub")
    user = await get_and_check_user(username)
    return SMeUser(
        name=user.name,
        email=user.email,
    )


async def get_current_user_by_refresh(
        payload: dict = Depends(get_token_payload),
) -> SLoginUser:
    check_token_type(payload, auth_jwt.REFRESH_TOKEN_TYPE)
    username: str | None = payload.get("sub")
    user = await get_and_check_user(username)
    return SLoginUser(
        name=user.name,
        password=user.password,
    )
