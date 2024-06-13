from fastapi import APIRouter
from pydantic import PositiveInt

from app.products.dao import ProductsDAO
from app.products.schemas import SProductWithCategory

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("")
async def get_products() -> list[SProductWithCategory]:
    products_with_categories = await ProductsDAO.get_products_with_categories()
    return products_with_categories


@router.get("{product_id}")
async def get_product(product_id: PositiveInt) -> SProductWithCategory:
    product_with_category = await ProductsDAO.get_product_with_category(product_id)
    return product_with_category
