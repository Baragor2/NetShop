from pydantic import BaseModel, PositiveInt, PositiveFloat


class SProduct(BaseModel):
    id: PositiveInt
    title: str
    description: str
    price: PositiveFloat
    image_id: PositiveInt
    category_id: PositiveInt
    characteristics: list


class SProductWithCategory(BaseModel):
    Products: SProduct
    name: str
