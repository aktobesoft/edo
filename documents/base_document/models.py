from enum import unique
from sqlalchemy import Column, String, Integer, Table, DateTime, Boolean, MetaData, ForeignKey, Date, event
from sqlalchemy.orm import relationship
from core.db import Base, metadata
from datetime import date, datetime
from pydantic import BaseModel, validator
from references.business_type.models import BusinessTypeOut, BusinessType
from references.document_type.models import DocumentType
from references.notes.models import Notes
from references.user.models import UserOut, User
from references.counterparty.models import Counterparty
from sqlalchemy.orm import declared_attr

class BaseDocument:

    id = Column(Integer, primary_key=True, autoincrement=True)
    guid = Column(String(36), nullable=False, index=True, unique=True)
    number = Column(String(150), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    comment = Column(String(350), nullable=True)
    sum = Column(Integer, nullable=True)

    @declared_attr
    def counterparty_id(cls):
        return Column(Integer, ForeignKey('counterparty.id', ondelete="CASCADE"), nullable=False)
    @declared_attr 
    def counterparty(cls):
        return relationship("Counterparty")

    @declared_attr
    def document_type_id(cls):
        return Column(Integer, ForeignKey('document_type.id', ondelete='CASCADE'), nullable=False)
    @declared_attr 
    def document_type(cls):
        return relationship("DocumentType")

    @declared_attr
    def entity_id(cls):
        return Column(Integer, ForeignKey('entity.id', ondelete="CASCADE"), nullable=False)
    @declared_attr 
    def entity(cls):
        return relationship("Entity")

class OptionsStructure(BaseModel):
    
    value: int
    text: str
    
    class Config:
        orm_mode = True

