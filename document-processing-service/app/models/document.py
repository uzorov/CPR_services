from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from enum import Enum
from models.base_model import Base


    # model_config = ConfigDict(from_attributes=True)
    # id: int
    # file_id: Optional[str]
    # subject: str
    # description: str
    # status: str
    # priority: str
    # author_id: UUID
    # responsible_employee_id: UUID
    # registration_date: datetime
    
class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    file_id = Column(String)
    subject = Column(String)
    description = Column(String)
    status = Column(String)
    priority = Column(String)
    author_id = Column(UUID)
    responsible_employee_id = Column(UUID)
    registration_date = Column(Date, default=datetime.utcnow().date)
