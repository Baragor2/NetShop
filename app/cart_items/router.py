from fastapi import APIRouter, Depends, status
from pydantic import PositiveInt

from app.cart_items.dao import CartItemsDAO
from app.cart_items.schemas import SCartItemWithProduct
from app.users.dependencies import get_current_user
from app.users.schemas import SMeUser

router = APIRouter(
    prefix="/cart_items",
    tags=["cart Items"],
)


@router.get("/me")
async def get_my_cart_items(
        current_user: SMeUser = Depends(get_current_user),
) -> list[SCartItemWithProduct]:
    cart_items = await CartItemsDAO.get_cart_items_with_product(current_user.name)
    return cart_items


@router.post("/{product_id}", status_code=status.HTTP_201_CREATED)
async def create_cart_item(
        quantity: PositiveInt,
        product_id: PositiveInt,
        current_user: SMeUser = Depends(get_current_user),
) -> dict:
    await CartItemsDAO.add_cart_item(current_user.name, product_id, quantity)
    return {"message": "Product has been successfully added to cart"}


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_item(
        product_id: PositiveInt,
        quantity: PositiveInt,
        current_user: SMeUser = Depends(get_current_user),
) -> None:
    await CartItemsDAO.remove_cart_item(current_user.name, product_id, quantity)
