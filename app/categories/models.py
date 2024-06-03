from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.products.models import Products


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    product = relationship('Products', order_by=Products.id, back_populates='category')
