from fastapi import APIRouter, status, Depends
from pydantic import PositiveInt

from app.products.dao import ProductsDAO
from app.products.schemas import SProductWithCategory, SProduct
from app.users.dependencies import check_admin_role, get_current_user
from app.users.schemas import SMeUser

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("/")
async def get_products() -> list[SProductWithCategory]:
    products_with_categories = await ProductsDAO.get_products_with_categories()
    return products_with_categories


@router.get("/{product_id}")
async def get_product(product_id: PositiveInt) -> SProductWithCategory:
    product_with_category = await ProductsDAO.get_product_with_category(product_id)
    return product_with_category


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
        product: SProduct,
        current_user: SMeUser = Depends(get_current_user),
) -> dict[str, str]:
    await ProductsDAO.create_product(product, current_user.name)
    return {"message": "Product created"}


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product_id: PositiveInt,
        current_user: SMeUser = Depends(get_current_user),
) -> None:
    await check_admin_role(current_user.name)
    await ProductsDAO.delete_product(product_id)


@router.put("/")
async def update_product(
        product: SProduct,
        current_user: SMeUser = Depends(get_current_user),
) -> dict[str, str]:
    await check_admin_role(current_user.name)

    await ProductsDAO.update_product(product)
    return {"message": "Product updated"}
