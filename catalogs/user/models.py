from tkinter.tix import Tree
from typing import Union
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean 
from sqlalchemy.orm import relationship 
from core.db import Base, metadata
from documents.base_document.models import Paginator

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True, autoincrement = True)
    email = Column(String, unique = True, index = True)
    name = Column(String(150), nullable = True)
    entity_iin = Column(String, ForeignKey('entity.iin'), nullable = True)
    entity = relationship("Entity")
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable = True)
    employee = relationship("Employee")
    hashed_password = Column(String)
    is_company = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.name, self.email)

class UserOut(BaseModel):
    
    id: int
    name: str
    email: EmailStr
    employee_id: Union[int, None]
    entity_iin: Union[str, None]
    employee_name: Union[str, None]
    entity_name: Union[str, None]
    is_active: bool
    is_company: bool
    hashed_password: Union[str, None] = ''

    class Config:
        orm_mode = True

class UserPUT(BaseModel):
    
    id: int
    name: str
    email: EmailStr
    employee_id: Union[int, None]
    entity_iin: Union[str, None]
    is_active: bool
    is_company: bool
    hashed_password: Union[str, None] = ''

    class Config:
        orm_mode = True

class UserPOST(BaseModel):
    
    name: str
    email: EmailStr
    employee_id: Union[int, None]
    entity_iin: Union[str, None]
    is_active: bool
    is_company: bool
    hashed_password: Union[str, None] = ''

    class Config:
        orm_mode = True

class UserListOut(BaseModel):
    info: Paginator
    result: list[UserOut]

class UserSmallOut(BaseModel):
    id: Union[int, None]
    name: Union[str, None]
    email: Union[str, None]

def fill_user_data_from_dict(queryResult : dict):
    return {
        'id': queryResult['user_id'],
        'name': queryResult['user_name'],
        'email': queryResult['user_email'],
        } 
def fill_assigned_user_data_from_dict(queryResult : dict):
    return {
        'id': queryResult['assigned_user_id'],
        'name': queryResult['assigned_user_name'],
        'email': queryResult['assigned_user_email'],
        } 
def fill_author_data_from_dict(queryResult : dict):
    return {
        'id': queryResult['author_id'],
        'name': queryResult['author_name'],
        'email': queryResult['author_email'],
        } 