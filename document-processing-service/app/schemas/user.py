from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class User(BaseModel):
    id: int
    full_name: str
    department: str
    organization: str
    password: str
    role_id: int
    
class Role(BaseModel):
    id: int
    role_code: str
    role_name: str