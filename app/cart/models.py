from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from app.database import Base


class Carts(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    username = Column(String(25), ForeignKey('users.name'), nullable=False)
    total_price = Column(DECIMAL, nullable=False, default=0)

    user = relationship('Users', back_populates='cart')

    def __str__(self):
        return f'Корзина: {self.id}'