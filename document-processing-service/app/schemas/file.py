from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class File(BaseModel):
    id: int
    file_name: str
    format: str
    user_id: int
    created_at: datetime