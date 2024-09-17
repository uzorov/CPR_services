from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from uuid import UUID

class Document(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    file_id: Optional[str]
    subject: str
    description: str
    status: str
    priority: str
    author_id: UUID
    responsible_employee_id: UUID
    registration_date: date
    
class DocumentCreate(BaseModel):
    file_id: Optional[str]
    file_id: Optional[str]
    subject: str
    description: str
    status: str
    priority: str
    author_id: UUID
    responsible_employee_id: UUID
    registration_date: Optional[date] = None

class DocumentUpdate(BaseModel):
    file_id: Optional[str]
    subject: Optional[str]
    description: Optional[str]
    status: Optional[str]
    priority: Optional[str]
    author_id: Optional[UUID]
    responsible_employee_id: Optional[UUID]
    registration_date: Optional[date]

