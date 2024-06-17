from sqlalchemy import Column, String, Boolean, LargeBinary
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    name = Column(String(25), primary_key=True)
    email = Column(String(254), nullable=False, unique=True)
    password = Column(LargeBinary, nullable=False)
    role = Column(String, nullable=False)
    active = Column(Boolean, nullable=False)

    cart_item = relationship('CartItems', back_populates='user')
    cart = relationship("Carts", back_populates="user")

    def __str__(self):
        return f"Пользователь: {self.name}"
