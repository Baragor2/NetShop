from fastapi import APIRouter, Depends, status

from app.cart.dao import CartsDAO
from app.users.dependencies import get_current_user
from app.users.schemas import SMeUser

router = APIRouter(
    prefix="/cart",
    tags=["Сart"],
)


@router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(current_user: SMeUser = Depends(get_current_user)):
    await CartsDAO.clear_cart(current_user.name)
