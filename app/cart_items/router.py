from fastapi import APIRouter, Depends

from app.cart_items.dao import CartItemsDAO
from app.cart_items.schemas import SCartItemWithProduct
from app.users.dependencies import get_current_user
from app.users.schemas import SMeUser

router = APIRouter(
    prefix="/cart_items",
    tags=["Cart Items"],
)


@router.get("/me")
async def get_my_cart_products(
        current_user: SMeUser = Depends(get_current_user)
) -> list[SCartItemWithProduct]:
    cart_items = await CartItemsDAO.get_cart_items_with_product(current_user.name)
    return cart_items
