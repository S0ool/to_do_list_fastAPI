from sqlalchemy import Text, String, Integer, DateTime, func
from sqlalchemy.testing.schema import Column
from database import Base

class ToDo(Base):
    __tablename__ = "to_dos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=255))
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())