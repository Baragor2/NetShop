from pydantic import PositiveInt
from sqlalchemy import update

from app.cart.models import Carts
from app.dao.base import BaseDAO
from app.database import async_session_maker


class CartsDAO(BaseDAO):
    model = Carts

    @classmethod
    async def add_price_from_cart_item(cls, username: str, cart_item_price: PositiveInt):
        async with async_session_maker() as session:
            stmt = (
                update(Carts)
                .where(Carts.username == username)
                .values(total_price=Carts.total_price + cart_item_price)
            )
            await session.execute(stmt)
            await session.commit()
