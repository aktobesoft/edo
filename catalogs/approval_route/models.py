from datetime import datetime
from typing import Union
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Index, String, Integer, Boolean, Enum 
from core.db import Base
from sqlalchemy.orm import relationship
import enum
from catalogs.approval_template.models import ApprovalTemplate
from catalogs.enum_types.models import EnumRouteStatusType
   
class ApprovalRoute(Base):
    __tablename__ = "approval_route"

    id = Column(Integer, primary_key = True, autoincrement = True)
    is_active = Column(Boolean, default=True)
    level = Column(Integer, nullable = False)
    type = Column(String, ForeignKey('enum_step_type.name'), nullable = True)
    enum_step_type = relationship("EnumStepType")
    document_id = Column(Integer, nullable = False, index = True)
    enum_document_type_id= Column(Integer, ForeignKey('enum_document_type.id'), nullable = False)
    entity_iin = Column(String, ForeignKey('entity.iin'), nullable = False, index = True)
    entity = relationship("Entity")
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False, index = True)
    user = relationship("User")
    approval_template_id = Column(Integer, ForeignKey('approval_template.id'), nullable = False, index = True)
    approval_template = relationship("ApprovalTemplate")
    approval_process_id = Column(Integer, ForeignKey('approval_process.id', ondelete = "CASCADE"), nullable = False, index = True)
    approval_process = relationship("ApprovalProcess")
    hash = Column(String, index = True)

    def __repr__(self) -> str:
        return self.name

Index('idx_ar_entity_document_id', ApprovalRoute.entity_iin, ApprovalRoute.document_id)

class ApprovalRouteOut(BaseModel):
    
    id: int
    is_active: bool
    level: int
    type: Union[str, None]
    document_id: int
    enum_document_type_id: int
    entity_iin: str
    user_id: int
    approval_template_id: int
    approval_process_id: int
    status_id: Union[int, None]
    status: Union[str, None]
    status_date: Union[datetime, None]
    status_comment: Union[str, None] = ''
    hash: Union[str, None] = ''
    
    class Config:
        orm_mode = True

class ApprovalRoutePUT(BaseModel):
    
    id: int
    is_active: bool
    level: int
    type: Union[str, None]
    document_id: int
    enum_document_type_id: int
    entity_iin: str
    user_id: int
    approval_template_id: int
    approval_process_id: int
    hash: Union[str, None] = ''
    
    class Config:
        orm_mode = True

class ApprovalRoutePOST(BaseModel):
    
    is_active: bool
    level: int
    type: Union[str, None]
    document_id: int
    enum_document_type_id: int
    entity_iin: str
    user_id: int
    approval_template_id: int
    approval_process_id: int
    hash: Union[str, None] = ''
    
    class Config:
        orm_mode = True

class ApprovalRouteNestedOut(BaseModel):
    
    id: int
    is_active: bool
    level: int
    type: Union[str, None]
    document_id: int
    enum_document_type_id: int
    entity_iin: str
    user_id: int
    user: dict
    approval_template_id: int
    approval_process_id: int
    status_id: Union[int, None]
    status: Union[str, None]
    status_date: Union[datetime, None]
    status_comment: Union[str, None] = ''
    hash: Union[str, None] = ''
    
    class Config:
        orm_mode = True

class ApprovalRouteIn(BaseModel):
    
    is_active: bool
    level: int
    type: Union[str, None]
    document_id: int
    enum_document_type_id: int
    entity_iin: str
    user_id: int
    approval_template_id: int
    approval_process_id: int
    hash: Union[str, None] = ''
    
    class Config:
        orm_mode = True