from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.products.models import Products


class Carts(Base):
    __tablename__ = 'carts'

    username = Column(String(25), primary_key=True)
    n = Column(String, nullable=False)

    products = relationship('Products', order_by=Products.id, back_populates='category')
