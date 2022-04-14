from datetime import datetime
from documents.base_document.models import BaseDocument
from core.db import Base
from pydantic import BaseModel

from references.counterparty.models import CounterpartySmallOut
from references.document_type.models import DocumentTypeOut
from references.entity.models import EntitySmallOut

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
    counterparty_id: int
    document_type_id: int
    entity_id: int
    
    class Config:
        orm_mode = True

class PurchaseRequisitionNestedOut(BaseModel):
    
    id: int
    guid: str
    number: str
    date: datetime
    comment: str
    sum: float
    counterparty_id: int
    document_type_id: int
    entity_id: int
    counterparty: CounterpartySmallOut
    document_type: DocumentTypeOut
    entity: EntitySmallOut
    
    class Config:
        orm_mode = True

class PurchaseRequisitionIn(BaseModel):
    
    guid: str
    number: str
    date: datetime
    comment: str
    sum: float
    counterparty_id: int
    document_type_id: int
    entity_id: int
    
    class Config:
        orm_mode = True