from datetime import datetime
from typing import Union
from pydantic import BaseModel
from sqlalchemy import Column, Float, String, Integer, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from documents.base_document.models import BaseDocument

from core.db import Base
from pydantic import BaseModel

from catalogs.counterparty.models import CounterpartySmallOut
from catalogs.enum_types.models import EnumDocumentTypeOut
from catalogs.entity.models import EntitySmallOut

class PurchaseRequisitionItems(Base):
    __tablename__ = "purchase_requisition_items"

    id = Column(Integer, primary_key = True, autoincrement = True) 
    service = Column(Boolean, nullable=True)
    description = Column(String(360), nullable = False)
    description_code = Column(String(36), nullable = False)
    quantity = Column(Float)
    sum = Column(Float)
    hash = Column(String, index = True)
    purchase_requisition_id = Column(Integer, ForeignKey('purchase_requisition.id'), index = True)
    purchase_requisition = relationship("PurchaseRequisition")

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.id, self.description)

class _PurchaseRequisitionItemsPUT(BaseModel):
    
    id: int
    service: bool
    description: str
    description_code: str
    quantity: float
    sum: float
    hash: Union[str, None] = ''
    
    class Config:
        orm_mode = True

class _PurchaseRequisitionItemsPOST(BaseModel):
    
    service: bool
    description: str
    description_code: str
    quantity: float
    sum: float
    hash: Union[str, None] = ''
    
    class Config:
        orm_mode = True

class _PurchaseRequisitionItemsOutWithLine(BaseModel):
    
    id: int
    line_number: int
    service: bool
    description: str
    description_code: str
    quantity: float
    sum: float
    
    class Config:
        orm_mode = True

class _PurchaseRequisitionItemsOut(BaseModel):
    
    id: int
    service: bool
    description: str
    description_code: str
    quantity: float
    sum: float
    
    class Config:
        orm_mode = True        

class _PurchaseRequisitionItemsSingleOut(BaseModel):
    
    id: int
    line_number: int
    service: bool
    description: str
    description_code: str
    quantity: float
    sum: float
    purchase_requisition_id: int
    
    class Config:
        orm_mode = True