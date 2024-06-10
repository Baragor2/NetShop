from pydantic import PositiveInt
from sqlalchemy import select

from app.cart.dao import CartsDAO
from app.cart_items.models import CartItems
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.products.dao import ProductsDAO
from app.products.models import Products
from app.products.schemas import SProduct
from app.users.schemas import SMeUser


class CartItemsDAO(BaseDAO):
    model = CartItems

    @classmethod
    async def get_cart_items_with_product(cls, username: str):
        """
        SELECT
            cart_items.*,
            products.*,
            cart_items.quantity * products.price AS total_price
        FROM
            cart_items
        JOIN
            products ON cart_items.product_id = products.id
        WHERE cart_items.username = 'username';
        """
        async with async_session_maker() as session:
            cart_items_with_product = (
                select(
                    Products,
                    CartItems,
                    (CartItems.quantity * Products.price).label('total_price')
                )
                .join(Products, CartItems.product_id == Products.id)
                .where(CartItems.username == username)
            )

            result = await session.execute(cart_items_with_product)
            return result.mappings().all()

    @classmethod
    async def add_cart_item(
            cls,
            current_username: str,
            product_id: PositiveInt,
            quantity: PositiveInt
    ) -> None:
        async with async_session_maker() as session:
            product: SProduct = await ProductsDAO.find_one_or_none(id=product_id)

            await CartItemsDAO.add(
                username=current_username,
                product_id=product_id,
                quantity=quantity,
            )
            await CartsDAO.add_price_from_cart_item(current_username, product.price * quantity)
            await session.commit()
