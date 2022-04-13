from pydantic import BaseModel
from sqlalchemy import Column, String, Integer 
from core.db import Base

class DocumentType(Base):
    __tablename__ = "document_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False, unique=True)
    description = Column(String(350), nullable=False)

    def __repr__(self) -> str:
        return self.description


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
