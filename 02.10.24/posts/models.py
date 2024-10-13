from sqlalchemy import Text, String, Integer, Column
from database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=255))
    description = Column(Text)
