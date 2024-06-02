from app.products.models import Products
from app.dao.base import BaseDAO


class ProductsDAO(BaseDAO):
    model = Products
