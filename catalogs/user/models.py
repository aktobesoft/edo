from typing import Union
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean 
from sqlalchemy.orm import relationship 
from core.db import Base, metadata
from documents.base_document.models import Paginator

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, autoincrement = True)
    email = Column(String, unique=True, index = True)
    name = Column(String(150), nullable=True)
    hashed_password = Column(String)
    is_company = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.name, self.email)

class UserOut(BaseModel):
    
    id: int
    name: str
    email: EmailStr
    is_active: bool
    is_company: bool
    entity_count: Union[int, None] = 0
    employee_count: Union[int, None] = 0
    hashed_password: Union[str, None] = ''

    class Config:
        orm_mode = True

class UserPUT(BaseModel):
    
    id: int
    name: str
    email: EmailStr
    is_active: bool
    is_company: bool
    hashed_password: Union[str, None] = ''

    class Config:
        orm_mode = True

class UserPOST(BaseModel):
    
    name: str
    email: EmailStr
    is_active: bool
    is_company: bool
    hashed_password: Union[str, None] = ''

    class Config:
        orm_mode = True

class UserListOut(BaseModel):
    info: Paginator
    result: list[UserOut]

def user_fillDataFromDict(queryResult : dict):
    return {
        'id': queryResult['user_id'],
        'name': queryResult['user_name'],
        'email': queryResult['user_email'],
        'is_active': queryResult['user_is_active'],
        'is_company': queryResult['user_is_company']
        } 