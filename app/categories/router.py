from fastapi import APIRouter
from fastapi.exceptions import ResponseValidationError

from app.categories.dao import CategoriesDAO
from app.categories.schemas import SCategory
from app.exceptions import NoSuchCategoryException
from app.products.dao import ProductsDAO
from app.products.schemas import SProductWithCategory

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get("/")
async def get_categories() -> list[SCategory]:
    categories = await CategoriesDAO.find_all()
    return categories


@router.get("/{category_id}")
async def get_category(category_id: int) -> SCategory:
    category = await CategoriesDAO.get_category(category_id)
    return category
