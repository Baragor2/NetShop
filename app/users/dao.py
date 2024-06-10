from app.cart.dao import CartsDAO
from app.database import async_session_maker
from app.users.models import Users
from app.dao.base import BaseDAO
from app.users.schemas import SRegisterUser


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def add_user_and_cart(cls, user_data: SRegisterUser, hashed_password: bytes) -> None:
        async with async_session_maker() as session:
            await UsersDAO.add(
                name=user_data.name,
                email=user_data.email,
                password=hashed_password,
                active=True,
                role="user",
            )

            await CartsDAO.add(
                username=user_data.name,
            )
            await session.commit()
