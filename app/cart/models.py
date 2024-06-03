from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database import Base


class CartItems(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    username = Column(String(25), ForeignKey('users.name'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    # user = relationship('Users', back_populates='cart_item')
    # product = relationship('Products', back_populates='cart_item')
