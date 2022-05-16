from datetime import datetime
from typing import Union

from sqlalchemy import null, union
from documents.base_document.models import BaseDocument, Paginator
from core.db import Base
from pydantic import BaseModel

from references.counterparty.models import CounterpartySmallOut
from references.document_type.models import DocumentTypeOut
from references.entity.models import EntitySmallOut
from documents.purchase_requisition_items.models import _PurchaseRequisitionItemsOut, _PurchaseRequisitionItemsPOST, _PurchaseRequisitionItemsPUT, _PurchaseRequisitionItemsOutWithLine
from references.enum_types.models import status_type

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
    status: Union[status_type, None]
    
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
    status: Union[status_type, None]
    items: list[_PurchaseRequisitionItemsOut]
    
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
    status: Union[status_type, None]
    entity: EntitySmallOut
    
    class Config:
        orm_mode = True

class PurchaseRequisitionNestedItemsOut(BaseModel):
    
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
    status: Union[status_type, None]
    items: list[_PurchaseRequisitionItemsOutWithLine]
    
    class Config:
        orm_mode = True

class PurchaseRequisitionListOut(BaseModel):
    info: Paginator
    result: list[PurchaseRequisitionOut]

class PurchaseRequisitionListNestedOut(BaseModel):
    info: Paginator
    result: list[PurchaseRequisitionNestedOut]

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
    items: list[_PurchaseRequisitionItemsPUT]
    
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
    items: list[_PurchaseRequisitionItemsPOST]
    
    class Config:
        orm_mode = True