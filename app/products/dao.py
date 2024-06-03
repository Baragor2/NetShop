from sqlalchemy import select

from app.categories.models import Categories
from app.database import async_session_maker
from app.products.models import Products
from app.dao.base import BaseDAO


class ProductsDAO(BaseDAO):
    model = Products

    @classmethod
    async def get_products_with_categories(cls):
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
