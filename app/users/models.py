from sqlalchemy import Column, String, Boolean, LargeBinary

from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    name = Column(String(25), primary_key=True)
    email = Column(String(254), nullable=False, unique=True)
    password = Column(LargeBinary, nullable=False)
    role = Column(String, nullable=False)
    active = Column(Boolean, nullable=False)
