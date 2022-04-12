from enum import unique
from sqlalchemy import Column, String, Integer, Table, DateTime, Boolean, MetaData, ForeignKey, Date, event
from sqlalchemy.orm import relationship
from core.db import Base, metadata
from datetime import date, datetime
from pydantic import BaseModel, validator
from .business_type import BusinessTypeOut, BusinessType
from .document_type import DocumentType
from .notes import Notes
from .user import UserOut, User
from .counterparty import Сounterparty
from sqlalchemy.orm import declared_attr

class BaseDocument:

    id = Column(Integer, primary_key=True, autoincrement=True)
    guid = Column(String(36), nullable=False, index=True, unique=True)
    number = Column(String(150), nullable=False)
    date = Column(DateTime, nullable=False)
    comment = Column(String(350), nullable=True)
    sum = Column(Integer, nullable=True)

    @declared_attr
    def counterparty_id(cls):
        return Column(Integer, ForeignKey('сounterparty.id', ondelete="CASCADE"), nullable=False)
    @declared_attr 
    def сounterparty(cls):
        return relationship("Сounterparty")

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

class PurchaseRequisition(BaseDocument, Base):
    __tablename__ = "purchase_requisition"

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.number, self.date)
