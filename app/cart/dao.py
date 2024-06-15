from pydantic import PositiveInt, NegativeInt
from sqlalchemy import update

from app.cart.models import Carts
from app.cart_items.dao import CartItemsDAO
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.schemas import Username


class CartsDAO(BaseDAO):
    model = Carts

    @classmethod
    async def change_price_from_cart_item(
            cls,
            username: Username,
            cart_item_price: PositiveInt | NegativeInt
    ) -> None:
        async with async_session_maker() as session:
            change_price_stmt = (
                update(Carts)
                .where(Carts.username == username)
                .values(total_price=Carts.total_price + cart_item_price)
            )
            await session.execute(change_price_stmt)
            await session.commit()

    @classmethod
    async def clear_cart(cls, username: Username) -> None:
        async with async_session_maker() as session:
            clear_cart_stmt = (
                update(Carts)
                .where(Carts.username == username)
                .values(total_price=0)
            )
            await session.execute(clear_cart_stmt)
            await CartItemsDAO.remove_all_cart_items_by_username(username)

            await session.commit()
