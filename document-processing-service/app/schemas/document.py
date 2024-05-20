from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class Document(BaseModel):
    id: int
    file_ids: Optional[List[int]]
    title: str
    body: str
    author_id: int
    responsible_employee_id: int
    created_at: datetime
    
class DocumentCreate(BaseModel):
    file_ids: Optional[List[int]]
    title: str
    body: str
    author_id: int
    responsible_employee_id: int
    created_at: Optional[datetime] = None

class DocumentUpdate(BaseModel):
    file_ids: Optional[List[int]]
    title: Optional[str]
    body: Optional[str]
    author_id: Optional[int]
    responsible_employee_id: Optional[int]
    created_at: Optional[datetime]