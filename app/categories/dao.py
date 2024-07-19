from pydantic import PositiveInt

from app.categories.models import Categories
from app.categories.schemas import SCategory
from app.dao.base import BaseDAO
from app.exceptions import NoSuchCategoryException
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