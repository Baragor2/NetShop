from pydantic import PositiveInt
from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound

from app.categories.models import Categories
from app.database import async_session_maker
from app.exceptions import NoSuchProductException
from app.products.models import Products
from app.dao.base import BaseDAO
from app.products.schemas import SProduct, SProductWithCategory


class ProductsDAO(BaseDAO):
    model = Products

    @classmethod
    async def get_products_with_categories(cls) -> list[SProductWithCategory]:
        """
        SELECT * FROM products
        JOIN categories ON products.category_id = categories.id
        """
        async with async_session_maker() as session:
            products_with_categories = (
                select(Products, Categories.name)
                .join(Categories, Products.category_id == Categories.id)
            )

            result = await session.execute(products_with_categories)
            return result.mappings().all()

    @classmethod
    async def get_product(cls, product_id: PositiveInt) -> SProduct:
        product = await ProductsDAO.find_one_or_none(id=product_id)
        if not product:
            raise NoSuchProductException
        return product

    @classmethod
    async def get_product_with_category(
            cls,
            product_id: PositiveInt,
    ) -> SProductWithCategory:
        """
        SELECT * FROM products
        JOIN categories ON products.category_id = categories.id
        WHERE products.id = ?
        """
        async with async_session_maker() as session:
            product_with_category = (
                select(Products, Categories.name)
                .join(Categories, Products.category_id == Categories.id)
                .where(Products.id == product_id)
            )
            result = await session.execute(product_with_category)

            try:
                return result.mappings().one()
            except NoResultFound:
                raise NoSuchProductException

    @classmethod
    async def get_products_by_categories(cls, category_name: str) -> list[SProductWithCategory | None]:
        """
        SELECT * FROM products
        JOIN categories ON products.category_id = categories.id
        WHERE categories.name = ?
        """
        async with async_session_maker() as session:
            products_with_categories = (
                select(Products, Categories.name)
                .join(Categories, Products.category_id == Categories.id)
                .where(Categories.name == category_name)
            )

            result = await session.execute(products_with_categories)
            return result.mappings().all()

    @classmethod
    async def delete_product(cls, product_id: PositiveInt) -> None:
        await cls.get_product(product_id)

        async with async_session_maker() as session:
            delete_product_stmt = (
                delete(Products)
                .where(Products.id == product_id)
            )

            await session.execute(delete_product_stmt)
            await session.commit()
