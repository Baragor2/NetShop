from pydantic import BaseModel, PositiveInt, PositiveFloat


class SProducts(BaseModel):
    id: PositiveInt
    title: str
    description: str
    price: PositiveFloat
    image_id: PositiveInt
    category_id: PositiveInt
    characteristics: list
