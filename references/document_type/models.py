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


class DocumentTypeOut(BaseModel): 
    
    id: int
    name: str
    description: str
    
    class Config:
        orm_mode = True

class DocumentTypeOptionsOut(BaseModel):
    
    value: int
    text: str
    
    class Config:
        orm_mode = True

def document_type_fillDataFromDict(queryResult : dict):
    return {
        'id': queryResult['document_type_id'],
        'name': queryResult['document_type_name'],
        'description': queryResult['document_type_description']
        }
