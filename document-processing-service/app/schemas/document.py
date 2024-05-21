from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum

class Document(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    file_id: Optional[str]
    title: str
    body: str
    author_id: int
    responsible_employee_id: int
    created_at: datetime
    
class DocumentCreate(BaseModel):
    file_id: Optional[str]
    title: str
    body: str
    author_id: int
    responsible_employee_id: int
    created_at: Optional[datetime] = None

class DocumentUpdate(BaseModel):
    file_id: Optional[str]
    title: Optional[str]
    body: Optional[str]
    author_id: Optional[int]
    responsible_employee_id: Optional[int]
    created_at: Optional[datetime]