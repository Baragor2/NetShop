from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, PositiveInt, PositiveFloat


class SCart(BaseModel):
    id: PositiveInt
    username: Annotated[str, MinLen(3), MaxLen(25)]
    total_price: PositiveFloat
