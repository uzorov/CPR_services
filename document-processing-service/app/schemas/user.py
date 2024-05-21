from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    department: str
    organization: str
    password: str
    role_id: int
    
class Role(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    role_code: str
    role_name: str