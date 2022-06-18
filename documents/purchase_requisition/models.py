from concurrent.futures import process
import datetime
from typing import Union

from sqlalchemy import null, union
from documents.base_document.models import BaseDocument, Paginator
from core.db import Base
from pydantic import BaseModel

from catalogs.counterparty.models import CounterpartySmallOut
from catalogs.document_type.models import DocumentTypeOut
from catalogs.entity.models import EntitySmallOut
from documents.purchase_requisition_items.models import _PurchaseRequisitionItemsOut, _PurchaseRequisitionItemsPOST, _PurchaseRequisitionItemsPUT, _PurchaseRequisitionItemsOutWithLine
from catalogs.enum_types.models import ProcessStatusType

class PurchaseRequisition(BaseDocument, Base):
    __tablename__ = "purchase_requisition"

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.number, self.date)

class PurchaseRequisitionOut(BaseModel):
    
    id: int
    guid: str
    number: str
    date: datetime.datetime
    comment: str
    sum: float
    counterparty_iin: str
    document_type_id: int
    entity_iin: str
    status: Union[str, None]
    approval_process_id: Union[int, None]
    approval_process_start_date: Union[datetime.date, None]
    approval_process_end_date: Union[datetime.date, None]
    
    class Config:
        orm_mode = True

class PurchaseRequisitionItemsOut(BaseModel):
    
    id: int
    guid: str
    number: str
    date: datetime.datetime
    sum: float
    counterparty_iin: str
    document_type_id: int
    entity_iin: str
    comment: str
    status: Union[str, None]
    approval_process_id: Union[int, None]
    approval_process_start_date: Union[datetime.date, None]
    approval_process_end_date: Union[datetime.date, None]
    items: list[_PurchaseRequisitionItemsOut]
    
    class Config:
        orm_mode = True

class PurchaseRequisitionNestedOut(BaseModel):
    
    id: int
    guid: str
    number: str
    date: datetime.datetime
    sum: float
    counterparty_iin: str
    document_type_id: int
    entity_iin: str
    counterparty: CounterpartySmallOut
    document_type: DocumentTypeOut
    comment: str
    status: Union[str, None]
    approval_process_id: Union[int, None]
    approval_process_start_date: Union[datetime.date, None]
    approval_process_end_date: Union[datetime.date, None]
    entity: EntitySmallOut
    
    class Config:
        orm_mode = True

class PurchaseRequisitionNestedOutWithRoutes(BaseModel):
    
    id: int
    guid: str
    number: str
    date: datetime.datetime
    sum: float
    counterparty_iin: str
    document_type_id: int
    entity_iin: str
    counterparty: CounterpartySmallOut
    document_type: DocumentTypeOut
    comment: str
    status: Union[str, None]
    approval_process_id: Union[int, None]
    approval_process_start_date: Union[datetime.date, None]
    approval_process_end_date: Union[datetime.date, None]
    entity: EntitySmallOut
    current_approval_routes: list
    all_approval_routes: list
    
    class Config:
        orm_mode = True

class PurchaseRequisitionNestedItemsOut(BaseModel):
    
    id: int
    guid: str
    number: str
    date: datetime.datetime
    sum: float
    counterparty_iin: str
    document_type_id: int
    entity_iin: str
    counterparty: CounterpartySmallOut
    document_type: DocumentTypeOut
    entity: EntitySmallOut
    comment: str
    status: Union[str, None]
    approval_process_id: Union[int, None]
    approval_process_start_date: Union[datetime.date, None]
    approval_process_end_date: Union[datetime.date, None]
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
    date: datetime.datetime
    comment: str
    sum: float
    counterparty_iin: str
    # document_type_id: int
    entity_iin: str
    items: list[_PurchaseRequisitionItemsPUT]
    
    class Config:
        orm_mode = True

class PurchaseRequisitionPOST(BaseModel):
    
    guid: str
    number: str
    date: datetime.datetime
    comment: str
    sum: float
    counterparty_iin: str
    # document_type_id: int
    entity_iin: str
    items: list[_PurchaseRequisitionItemsPOST]
    
    class Config:
        orm_mode = True