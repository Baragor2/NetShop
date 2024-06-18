from app.categories.models import Categories
from app.dao.base import BaseDAO


class CategoriesDAO(BaseDAO):
    model = Categories
