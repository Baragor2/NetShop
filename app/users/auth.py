from datetime import UTC, datetime, timedelta

import jwt
import bcrypt

from app.config import settings, auth_jwt
from app.exceptions import UserAlreadyExistsException
from app.users.dao import UsersDAO
from app.users.schemas import SLoginUser


def encode_jwt(
    payload: dict,
    private_key: str = auth_jwt.private_key_pass.read_text(),
    algorithm: str = settings.ALGORITHM,
    expire_minutes: int = auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None
):
    to_encode = payload.copy()

    now = datetime.now(UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = auth_jwt.public_key_pass.read_text(),
    algorithm: str = settings.ALGORITHM,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


async def check_exists(user_data) -> None:
    existing_user = await UsersDAO.find_one_or_none(name=user_data.name)
    if not existing_user:
        existing_user = await UsersDAO.find_one_or_none(email=user_data.email)

    if existing_user:
        raise UserAlreadyExistsException


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None
) -> str:
    jwt_payload = {auth_jwt.TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: SLoginUser) -> str:
    jwt_payload = {"sub": user.name}
    return create_jwt(
        token_type=auth_jwt.ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def create_refresh_token(user: SLoginUser) -> str:
    jwt_payload = {"sub": user.name}
    return create_jwt(
        token_type=auth_jwt.REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=auth_jwt.REFRESH_TOKEN_EXPIRE_DAYS)
    )
