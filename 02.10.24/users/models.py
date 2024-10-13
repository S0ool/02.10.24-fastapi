from database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_user: Mapped[bool] = mapped_column(Boolean, default=True, server_default='true', nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default='false', nullable=False)
