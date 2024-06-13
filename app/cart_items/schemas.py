from pydantic import BaseModel, PositiveInt, PositiveFloat

from app.products.schemas import SProduct
from app.users.schemas import Username


class SCartItem(BaseModel):
    id: PositiveInt
    username: Username
    product_id: PositiveInt
    quantity: PositiveInt


class SCartItemWithProduct(BaseModel):
    Products: SProduct
    CartItems: SCartItem
    total_price: PositiveFloat
