from pydantic import BaseModel, PositiveInt

from app.users.schemas import Username


class SOrder(BaseModel):
    id: PositiveInt
    name: Username
    cart_id: PositiveInt
