from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from uuid import UUID
from datetime import datetime
from enum import Enum
from app.models.base_model import Base

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    file_ids = Column(String)
    title = Column(String)
    body = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", foreign_keys=[author_id], backref="authored_documents")
    responsible_employee_id = Column(Integer, ForeignKey('users.id'))
    responsible_employee = relationship("User", foreign_keys=[responsible_employee_id], backref="responsible_documents")
    created_at = Column(DateTime, default=datetime.utcnow)