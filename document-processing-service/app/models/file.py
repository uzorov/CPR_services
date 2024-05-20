from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from uuid import UUID
from datetime import datetime
from enum import Enum
from app.models.base_model import Base

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    format = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="files")
    created_at = Column(DateTime, default=datetime.utcnow)