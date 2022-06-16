from importlib.metadata import metadata
from operator import index
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, true 
from core.db import Base
from documents.base_document.models import Paginator

class DocumentType(Base):
    __tablename__ = "document_type"

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(150), nullable = False, unique=True)
    metadata_name = Column(String(150), nullable = True, unique=True)
    description = Column(String(350), nullable = False)

    def __repr__(self) -> str:
        return self.description


class DocumentTypeOut(BaseModel): 
    
    id: int = 0
    name: str = ''
    metadata_name: str = ''
    description: str = ''
    
    class Config:
        orm_mode = True

class DocumentTypeIn(BaseModel): 
    
    name: str = ''
    description: str = ''
    metadata_name: str = ''
    
    class Config:
        orm_mode = True

class DocumentTypeOptionsOut(BaseModel):
    
    value: int
    text: str
    
    class Config:
        orm_mode = True

class DocumentTypeListOut(BaseModel):
    info: Paginator
    result: list[DocumentTypeOut]

def document_type_fillDataFromDict(queryResult : dict):
    return {
        'id': queryResult['document_type_id'],
        'name': queryResult['document_type_name'],
        'description': queryResult['document_type_description']
        }
