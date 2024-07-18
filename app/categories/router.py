from fastapi import APIRouter

from app.categories.dao import CategoriesDAO
from app.categories.schemas import SCategory
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


# @router.get("/{category_name}")
# async def get_products_by_category(category_name: str) -> list[SProductWithCategory]:
#     products_with_categories = await ProductsDAO.get_products_by_categories(category_name)
#     return products_with_categories


@router.get("/{category_id}")
async def get_category(category_id: int) -> SCategory:
    category = await CategoriesDAO.find_one_or_none(id=category_id)
    return category
