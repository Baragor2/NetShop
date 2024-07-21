from pydantic import PositiveInt
from sqlalchemy import delete

from app.categories.models import Categories
from app.categories.schemas import SCategory
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import NoSuchCategoryException, ProductsWithSuchCategoryException
from app.users.dependencies import check_admin_role
from app.users.schemas import Username


class CategoriesDAO(BaseDAO):
    model = Categories

    @classmethod
    async def get_category(cls, category_id: PositiveInt) -> SCategory:
        category = await CategoriesDAO.find_one_or_none(id=category_id)
        if not category:
            raise NoSuchCategoryException
        return category

    @classmethod
    async def create_category(cls, category: SCategory, username: Username) -> None:
        await check_admin_role(username)
        await CategoriesDAO.add(**dict(category))

    @classmethod
    async def delete_category(cls, category_id: PositiveInt) -> None:
        from app.products.dao import ProductsDAO

        products = await ProductsDAO.find_all(category_id=category_id)
        if products:
            raise ProductsWithSuchCategoryException

        await cls.get_category(category_id)

        async with async_session_maker() as session:
            delete_category_stmt = (
                delete(Categories)
                .where(Categories.id == category_id)
            )

        await session.execute(delete_category_stmt)
        await session.commit()
