from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import PositiveInt, NegativeInt
from sqlalchemy import update

from app.cart.models import Carts
from app.dao.base import BaseDAO
from app.database import async_session_maker


class CartsDAO(BaseDAO):
    model = Carts

    @classmethod
    async def change_price_from_cart_item(
            cls,
            username: Annotated[str, MinLen(3), MaxLen(25)],
            cart_item_price: PositiveInt | NegativeInt
    ) -> None:
        async with async_session_maker() as session:
            stmt = (
                update(Carts)
                .where(Carts.username == username)
                .values(total_price=Carts.total_price + cart_item_price)
            )
            await session.execute(stmt)
            await session.commit()
