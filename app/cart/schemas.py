from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, PositiveInt


class SCartItems(BaseModel):
    id: PositiveInt
    username: Annotated[str, MinLen(3), MaxLen(25)]
    product_id: PositiveInt
    quantity: PositiveInt
