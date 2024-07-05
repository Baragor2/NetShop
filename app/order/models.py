from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    username = Column(String(25), ForeignKey('users.name'), nullable=False, unique=True)
    cart_id = Column(Integer, ForeignKey('carts.id'),  nullable=False)

    def __str__(self):
        return f"Заказ: {self.id}"
