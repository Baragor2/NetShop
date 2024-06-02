from pydantic import BaseModel, PositiveInt


class SCategories(BaseModel):
    id: PositiveInt
    name: str
