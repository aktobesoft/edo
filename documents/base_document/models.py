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
    sum = Column(Float, nullable=True)

    @declared_attr
    def counterparty_iin(cls):
        return Column(String, ForeignKey('counterparty.iin'), nullable = False, index = True)
    @declared_attr 
    def counterparty(cls):
        return relationship("Counterparty")

    @declared_attr
    def document_type_id(cls):
        return Column(Integer, ForeignKey('document_type.id', ondelete='CASCADE'), nullable = False)
    @declared_attr 
    def document_type(cls):
        return relationship("DocumentType")

    @declared_attr
    def entity_iin(cls):
        return Column(String, ForeignKey('entity.iin'), nullable = False, index = True)
    @declared_attr 
    def entity(cls):
        return relationship("Entity")

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


