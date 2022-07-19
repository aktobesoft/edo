from concurrent.futures import process
import datetime
from typing import Union

from sqlalchemy import Column, String
from catalogs.user.models import UserSmallOut
from documents.base_document.models import BaseDocument, Paginator
from core.db import Base
from pydantic import BaseModel

from catalogs.counterparty.models import CounterpartySmallOut
from catalogs.enum_types.models import EnumDocumentTypeOut
from catalogs.entity.models import EntitySmallOut

class EmployeeTask(BaseDocument, Base):
    __tablename__ = "employee_task"

    content = Column(String, nullable=True)

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.number, self.date)

class EmployeeTaskOut(BaseModel):
    
    id: int
    guid: str
    number: str
    date: datetime.datetime
    comment: str
    content: Union[str, None]
    enum_document_type_id: int
    author_id: Union[int, None]
    assigned_user_id: Union[int, None]
    entity_iin: str
    status: Union[str, None]
    status_date: Union[datetime.date, None]
    
    class Config:
        orm_mode = True

class EmployeeTaskNestedOut(BaseModel):
    
    id: int
    guid: str
    number: str
    date: datetime.datetime
    enum_document_type_id: int
    entity_iin: str
    entity: EntitySmallOut
    author_id: Union[int, None]
    author: UserSmallOut
    assigned_user_id: Union[int, None]
    assigned_user: UserSmallOut
    enum_document_type: EnumDocumentTypeOut
    comment: str
    content: Union[str, None]
    status: Union[str, None]
    status_date: Union[datetime.date, None]
    status_comment: Union[str, None]
    
    class Config:
        orm_mode = True

class EmployeeTaskNestedOutWithAllStatus(BaseModel):
    
    id: int
    guid: str
    number: str
    date: datetime.datetime
    enum_document_type_id: int
    entity_iin: str
    entity: EntitySmallOut
    author_id: Union[int, None]
    author: UserSmallOut
    assigned_user_id: Union[int, None]
    assigned_user: UserSmallOut
    enum_document_type: EnumDocumentTypeOut
    comment: str
    content: Union[str, None]
    status: Union[str, None]
    status_date: Union[datetime.date, None]
    status_comment: Union[str, None]
    last_task_status: Union[dict, None]
    all_task_status: list
    
    class Config:
        orm_mode = True

class EmployeeTaskListOut(BaseModel):
    info: Paginator
    result: list[EmployeeTaskOut]

class EmployeeTaskListNestedOut(BaseModel):
    info: Paginator
    result: list[EmployeeTaskNestedOut]

class EmployeeTaskPUT(BaseModel):
    
    id: int
    number: Union[str, None]
    guid: Union[str, None]
    date: datetime.datetime
    comment: Union[str, None]
    content: Union[str, None]
    entity_iin: str
    
    class Config:
        orm_mode = True

class EmployeeTaskPOST(BaseModel):
    
    guid: Union[str, None]
    date: datetime.datetime
    comment: Union[str, None]
    content: Union[str, None]
    entity_iin: str
    
    class Config:
        orm_mode = True