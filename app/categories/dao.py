from app.categories.models import Categories
from app.dao.base import BaseDAO
from app.exceptions import NoSuchCategoryException


class CategoriesDAO(BaseDAO):
    model = Categories

    @classmethod
    async def get_category(cls, category_id):
        category = await CategoriesDAO.find_one_or_none(id=category_id)
        if not category:
            raise NoSuchCategoryException
        return category
