import datetime
from typing import Union

from sqlalchemy import Column, Float, ForeignKey, String
from catalogs.user.models import UserSmallOut
from documents.base_document.models import BaseDocument, Paginator
from core.db import Base
from pydantic import BaseModel

from catalogs.counterparty.models import CounterpartySmallOut
from catalogs.enum_types.models import EnumDocumentTypeOut
from catalogs.entity.models import EntitySmallOut
from sqlalchemy.orm import relationship
from documents.purchase_requisition_items.models import _PurchaseRequisitionItemsOut, _PurchaseRequisitionItemsPOST, _PurchaseRequisitionItemsPUT, _PurchaseRequisitionItemsOutWithLine
from catalogs.enum_types.models import EnumProcessStatusType

class PurchaseRequisition(BaseDocument, Base):
    __tablename__ = "purchase_requisition"

    sum = Column(Float, nullable=True)
    counterparty_iin = Column(String, ForeignKey('counterparty.iin'), nullable = False, index = True)
    counterparty = relationship("Counterparty")

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
    enum_document_type_id: int
    entity_iin: str
    author_id: Union[int, None]
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
    enum_document_type_id: int
    entity_iin: str
    author_id: Union[int, None]
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
    enum_document_type_id: int
    entity_iin: str
    author_id: Union[int, None]
    author: UserSmallOut
    counterparty: CounterpartySmallOut
    enum_document_type: EnumDocumentTypeOut
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
    enum_document_type_id: int
    entity_iin: str
    author_id: Union[int, None]
    author: UserSmallOut
    counterparty: CounterpartySmallOut
    enum_document_type: EnumDocumentTypeOut
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

class PurchaseRequisitionNestedItemsOutWithRoutes(BaseModel):
    
    id: int
    guid: str
    number: str
    date: datetime.datetime
    sum: float
    counterparty_iin: str
    enum_document_type_id: int
    entity_iin: str
    author_id: Union[int, None]
    author: UserSmallOut
    counterparty: CounterpartySmallOut
    enum_document_type: EnumDocumentTypeOut
    comment: str
    status: Union[str, None]
    approval_process_id: Union[int, None]
    approval_process_start_date: Union[datetime.date, None]
    approval_process_end_date: Union[datetime.date, None]
    entity: EntitySmallOut
    current_approval_routes: list
    all_approval_routes: list
    items: list[_PurchaseRequisitionItemsOutWithLine]
    
    class Config:
        orm_mode = True

class PurchaseRequisitionNestedItemsOut(BaseModel):
    
    id: int
    guid: str
    number: str
    date: datetime.datetime
    sum: float
    counterparty_iin: str
    enum_document_type_id: int
    entity_iin: str
    counterparty: CounterpartySmallOut
    enum_document_type: EnumDocumentTypeOut
    entity: EntitySmallOut
    author_id: Union[int, None]
    author: UserSmallOut
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
    # enum_document_type_id: int
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
    # enum_document_type_id: int
    entity_iin: str
    items: list[_PurchaseRequisitionItemsPOST]
    
    class Config:
        orm_mode = True