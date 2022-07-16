from sqlalchemy import Column, Float, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from sqlalchemy.orm import declared_attr

class BaseDocument:

    id = Column(Integer, primary_key = True, autoincrement = True)
    guid = Column(String(36), nullable = False, index = True)
    number = Column(String(150), nullable = False)
    date = Column(DateTime(timezone=True), nullable = False)
    comment = Column(String(350), nullable=True)

    @declared_attr
    def enum_document_type_id(cls):
        return Column(Integer, ForeignKey('enum_document_type.id', ondelete='CASCADE'), nullable = False)
    @declared_attr 
    def enum_document_type(cls):
        return relationship("EnumDocumentType")

    @declared_attr
    def entity_iin(cls):
        return Column(String, ForeignKey('entity.iin'), nullable = False, index = True)
    @declared_attr 
    def entity(cls):
        return relationship("Entity")

    @declared_attr
    def author_id(cls):
        return Column(Integer, ForeignKey('user.id'))
    @declared_attr 
    def author(cls):
        return relationship("User")

class OptionsStructure(BaseModel):
    
    value: int
    text: str
    
    class Config:
        orm_mode = True

class OptionsStructureStr(BaseModel):
    
    value: str
    text: str
    
    class Config:
        orm_mode = True

class Paginator(BaseModel):

    pages: int = 1
    page: int = 1
    limit: int = 100
    has_previous: bool = False
    has_next : bool = False

    class Config:
        orm_mode = True


