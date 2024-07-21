from fastapi import APIRouter, Depends, status
from pydantic import PositiveInt

from app.categories.dao import CategoriesDAO
from app.categories.schemas import SCategory
from app.users.dependencies import get_current_user, check_admin_role
from app.users.schemas import SUser

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get("/")
async def get_categories() -> list[SCategory]:
    categories = await CategoriesDAO.find_all()
    return categories


@router.get("/{category_id}")
async def get_category(category_id: PositiveInt) -> SCategory:
    category = await CategoriesDAO.get_category(category_id)
    return category


@router.post("/")
async def create_category(
        category: SCategory,
        current_user: SUser = Depends(get_current_user),
) -> dict[str, str]:
    await check_admin_role(current_user.name)
    await CategoriesDAO.create_category(category, current_user.name)
    return {"message": "Category created"}


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
        category_id: PositiveInt,
        current_user: SUser = Depends(get_current_user),
) -> None:
    await check_admin_role(current_user.name)
    await CategoriesDAO.delete_category(category_id)
