from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum

class File(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    file_name: str
    format: str
    user_id: int
    created_at: datetime