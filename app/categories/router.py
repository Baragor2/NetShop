from fastapi import APIRouter, Depends

from app.categories.dao import CategoriesDAO
from app.categories.schemas import SCategory
from app.users.dependencies import get_current_user
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
async def get_category(category_id: int) -> SCategory:
    category = await CategoriesDAO.get_category(category_id)
    return category


@router.post("/")
async def create_category(
        category: SCategory,
        current_user: SUser = Depends(get_current_user),
) -> dict[str, str]:
    await CategoriesDAO.create_category(category, current_user.name)
    return {"message": "Category created"}
