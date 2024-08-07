from pydantic import PositiveInt
from sqlalchemy import select, delete, update
from sqlalchemy.exc import NoResultFound

from app.categories.models import Categories
from app.database import async_session_maker
from app.exceptions import NoSuchProductException
from app.products.models import Products
from app.dao.base import BaseDAO
from app.products.schemas import SProduct, SProductWithCategory
from app.users.dependencies import check_admin_role
from app.users.schemas import Username
from app.categories.dao import CategoriesDAO


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

    @classmethod
    async def create_product(cls, product: SProduct, username: Username):
        await CategoriesDAO.get_category(product.category_id)
        await check_admin_role(username)
        await ProductsDAO.add(**dict(product))

    @classmethod
    async def update_product(cls, product: SProduct):
        await cls.get_product(product.id)
        await CategoriesDAO.get_category(product.category_id)

        async with async_session_maker() as session:
            update_product_stmt = (
                update(Products)
                .where(Products.id == product.id)
                .values(**dict(product))
            )

        await session.execute(update_product_stmt)
        await session.commit()
