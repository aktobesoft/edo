from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean 
from core.db import Base, metadata

class BusinessType(Base):
    __tablename__ = "business_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True)
    full_name = Column(String(360))

    def __repr__(self) -> str:
        return self.name
        

class BusinessTypeOut(BaseModel):
    
    id: int
    name: str
    full_name: str
    
    class Config:
        orm_mode = True

class BusinessTypeOptionsOut(BaseModel):
    
    value: int
    text: str
    
    class Config:
        orm_mode = True