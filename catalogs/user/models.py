from pydantic import BaseModel, EmailStr, validator
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import relationship 
from core.db import Base, metadata

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

    class Config:
        orm_mode = True

class UserIn(BaseModel):
    
    name: str
    email: EmailStr
    is_active: bool
    is_company: bool

    class Config:
        orm_mode = True


class UserOptionsOut(BaseModel):
    
    value: int
    text: EmailStr
    
    class Config:
        orm_mode = True

def user_fillDataFromDict(queryResult : dict):
    return {
        'id': queryResult['user_id'],
        'name': queryResult['user_name'],
        'email': queryResult['user_email'],
        'is_active': queryResult['user_is_active'],
        'is_company': queryResult['user_is_company']
        } 