from pydantic import PositiveInt, NegativeInt
from sqlalchemy import select, and_, update, delete, Update, Delete

from app.cart import dao as cart_dao
from app.cart_items.models import CartItems
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import NoSuchProductInCartException
from app.products.dao import ProductsDAO
from app.products.models import Products
from app.products.schemas import SProduct
from app.users.schemas import Username


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
    async def _make_update_request(
            cls,
            current_username: str,
            product_id: PositiveInt,
            quantity: PositiveInt | NegativeInt,
    ) -> Update:
        update_query = (
            update(CartItems)
            .where(
                and_(
                    CartItems.username == current_username,
                    CartItems.product_id == product_id,
                )
            )
            .values(quantity=CartItems.quantity + quantity)
        )
        return update_query

    @classmethod
    async def _make_delete_request(
            cls,
            current_username: str,
            product_id: PositiveInt,
    ) -> Delete:
        delete_query = (
            delete(CartItems)
            .where(
                and_(
                    CartItems.username == current_username,
                    CartItems.product_id == product_id,
                )
            )
        )
        return delete_query

    @classmethod
    async def add_cart_item(
            cls,
            current_username: str,
            product_id: PositiveInt,
            quantity: PositiveInt,
    ) -> None:
        async with async_session_maker() as session:
            product: SProduct = await ProductsDAO.get_product(product_id)

            cart_item: CartItems | None = await CartItemsDAO.find_one_or_none(
                username=current_username,
                product_id=product_id,
            )
            if not cart_item:
                await CartItemsDAO.add(
                    username=current_username,
                    product_id=product_id,
                    quantity=quantity,
                )
            else:
                update_query: Update = await cls._make_update_request(
                    current_username,
                    product_id,
                    quantity,
                )
                await session.execute(update_query)

            await cart_dao.CartsDAO.change_price_from_cart_item(current_username, product.price * quantity)
            await session.commit()

    @classmethod
    async def remove_cart_item(
            cls,
            current_username: Username,
            product_id: PositiveInt,
            quantity: PositiveInt,
    ) -> None:
        async with async_session_maker() as session:
            product: SProduct = await ProductsDAO.get_product(product_id)

            cart_item: CartItems | None = await CartItemsDAO.find_one_or_none(
                username=current_username,
                product_id=product_id,
            )
            if not cart_item:
                raise NoSuchProductInCartException
            elif cart_item.quantity <= quantity:
                delete_query = await cls._make_delete_request(
                    current_username,
                    product_id,
                )
                await session.execute(delete_query)
                await cart_dao.CartsDAO.change_price_from_cart_item(
                    current_username,
                    -(product.price * cart_item.quantity),
                )
            else:
                update_query: Update = await cls._make_update_request(
                    current_username,
                    product_id,
                    -quantity,
                )
                await session.execute(update_query)
                await cart_dao.CartsDAO.change_price_from_cart_item(
                    current_username,
                    -(product.price * quantity)
                )
            await session.commit()

    @classmethod
    async def remove_all_cart_items_by_username(cls, username: Username) -> None:
        async with async_session_maker() as session:
            remove_cart_items_stmt = (
                delete(CartItems)
                .where(CartItems.username == username)
            )
            await session.execute(remove_cart_items_stmt)
            await session.commit()
