from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from uuid import UUID
from datetime import datetime
from enum import Enum
from app.models.base_model import Base


class UserRole(Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    department = Column(String)
    organization = Column(String)
    password = Column(String)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role", back_populates="users")

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role_code = Column(String)
    role_name = Column(String)
    users = relationship("User", back_populates="role")