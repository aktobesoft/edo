from datetime import datetime, date
from typing import Any, Union
from pydantic import BaseModel
from sqlalchemy import Column, Date, Enum, ForeignKey, String, Integer, Boolean, DateTime, null
from core.db import Base
from sqlalchemy.orm import relationship
from references.approval_route.models import ApprovalRouteNestedOut, ApprovalRouteOut, ApprovalRoutePOST, ApprovalRoutePUT
from references.enum_types.models import step_type, status_type
   
class ApprovalProcess(Base):
    __tablename__ = "approval_process"

    id = Column(Integer, primary_key = True, autoincrement = True)
    is_active = Column(Boolean, default=True)
    document_id = Column(Integer, nullable = False, index = True)
    document_type_id= Column(Integer, ForeignKey('document_type.id', ondelete = "CASCADE"), nullable = False)
    entity_iin = Column(String, ForeignKey('entity.iin', ondelete = "CASCADE"), nullable = False, index = True)
    entity = relationship("Entity")
    start_date = Column(Date, nullable = True, default=datetime.utcnow)
    end_date = Column(Date, nullable = True)
    approval_template_id = Column(Integer, ForeignKey('approval_template.id', ondelete = "CASCADE"), nullable = False, index = True)
    approval_template = relationship("ApprovalTemplate")
    status = Column(Enum(status_type), index = True, default = status_type.draft)


class ApprovalProcessOut(BaseModel):
    
    id: int
    is_active: bool
    document_id: int
    document_type_id: int
    entity_iin: str
    approval_template_id: int
    status: Union[status_type, None]
    start_date: date = None
    end_date: date = None
    
    class Config:
        orm_mode = True

class ApprovalProcessNestedOut(BaseModel):
    
    id: int
    is_active: bool
    document_id: int
    document_type_id: int
    entity_iin: str
    approval_template_id: int
    status: Union[status_type, None]
    start_date: date = None
    end_date: date = None
    document: dict
    document_type: dict
    entity: dict
    approval_template: dict

class ApprovalProcessRoutOut(BaseModel):
    
    id: int
    is_active: bool
    document_id: int
    document_type_id: int
    entity_iin: str
    approval_template_id: int
    status: Union[status_type, None]
    start_date: date = None
    end_date: date = None
    routes: list[ApprovalRouteOut]
    
    class Config:
        orm_mode = True

class ApprovalProcessRoutPUT(BaseModel):
    
    id: int
    is_active: bool
    document_id: int
    document_type_id: int
    entity_iin: str
    approval_template_id: int
    status: status_type = status_type.in_process
    start_date: date = None
    end_date: date = None
    routes: list[ApprovalRoutePUT]
    
    class Config:
        orm_mode = True

class ApprovalProcessRoutPOST(BaseModel):
    
    is_active: bool
    document_id: int
    document_type_id: int
    entity_iin: str
    approval_template_id: int
    status: status_type = status_type.in_process
    start_date: date = None
    end_date: date = None
    routes: list[ApprovalRoutePOST]
    
    class Config:
        orm_mode = True

class ApprovalProcessRoutNestedOut(BaseModel):
    
    id: int
    is_active: bool
    document_id: int
    document_type_id: int
    entity_iin: str
    approval_template_id: int
    status: Union[status_type, None]
    start_date: date = None
    end_date: date = None
    document: dict
    document_type: dict
    entity: dict
    approval_template: dict
    routes: list[ApprovalRouteNestedOut]
    
    class Config:
        orm_mode = True

class ApprovalProcessIn(BaseModel):
    
    is_active: bool
    document_id: int
    document_type_id: int
    entity_iin: str
    approval_template_id: int
    status: status_type
    start_date: date = None
    end_date: date = None
    
    class Config:
        orm_mode = True

class ApprovalProcessCheck(BaseModel):
    
    is_active: bool
    document_id: list[int]
    document_type_id: int
    entity_iin: str

