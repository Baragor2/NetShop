from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(DECIMAL, nullable=False)
    image_id = Column(Integer)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    characteristics = Column(JSON, nullable=False)

    category = relationship('Categories', back_populates='products')
