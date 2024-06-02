from typing import Literal, Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr


class SMeUser(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(25)]
    email: Annotated[EmailStr, MaxLen(254)]


class SUsers(SMeUser):
    password: Annotated[bytes, MinLen(8)]
    role: Literal["admin", "user"] = "user"
    active: bool = True


class SLoginUser(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(25)]
    password: Annotated[str, MinLen(8)]


class SRegisterUser(SLoginUser):
    email: EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
