from datetime import datetime
from documents.base_document.models import BaseDocument
from core.db import Base
from pydantic import BaseModel

from references.counterparty.models import CounterpartySmallOut
from references.document_type.models import DocumentTypeOut
from references.entity.models import EntitySmallOut
from documents.purchase_requisition_items.models import PurchaseRequisitionItemsPUT, PurchaseRequisitionItemsOutWithLine, PurchaseRequisitionItemsPOST

class PurchaseRequisition(BaseDocument, Base):
    __tablename__ = "purchase_requisition"

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.number, self.date)

class PurchaseRequisitionOut(BaseModel):
    
    id: int
    guid: str
    number: str
    date: datetime
    comment: str
    sum: float
    counterparty_iin: str
    document_type_id: int
    entity_iin: str
    
    class Config:
        orm_mode = True

class PurchaseRequisitionItemsOut(BaseModel):
    
    id: int
    guid: str
    number: str
    date: datetime
    comment: str
    sum: float
    counterparty_iin: str
    document_type_id: int
    entity_iin: str
    items: list[PurchaseRequisitionItemsOutWithLine]
    
    class Config:
        orm_mode = True

class PurchaseRequisitionNestedOut(BaseModel):
    
    id: int
    guid: str
    number: str
    date: datetime
    comment: str
    sum: float
    counterparty_iin: str
    document_type_id: int
    entity_iin: str
    counterparty: CounterpartySmallOut
    document_type: DocumentTypeOut
    entity: EntitySmallOut
    items: list[PurchaseRequisitionItemsOutWithLine]
    
    class Config:
        orm_mode = True

class PurchaseRequisitionPUT(BaseModel):
    
    id: int
    guid: str
    number: str
    date: datetime
    comment: str
    sum: float
    counterparty_iin: str
    document_type_id: int
    entity_iin: str
    items: list[PurchaseRequisitionItemsPUT]
    
    class Config:
        orm_mode = True

class PurchaseRequisitionPOST(BaseModel):
    
    guid: str
    number: str
    date: datetime
    comment: str
    sum: float
    counterparty_iin: str
    document_type_id: int
    entity_iin: str
    items: list[PurchaseRequisitionItemsPOST]
    
    class Config:
        orm_mode = True