from fastapi import APIRouter

from app.products.dao import ProductsDAO

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("")
async def get_products():
    products_with_categories = await ProductsDAO.get_products_with_categories()
    return products_with_categories
