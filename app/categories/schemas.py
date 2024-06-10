from pydantic import BaseModel, PositiveInt


class SCategory(BaseModel):
    id: PositiveInt
    name: str
