from pydantic import BaseModel, PositiveInt, PositiveFloat

from app.users.schemas import Username


class SCart(BaseModel):
    id: PositiveInt
    username: Username
    total_price: PositiveFloat
