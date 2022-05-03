from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Index, String, Integer, Boolean, Enum 
from core.db import Base
from sqlalchemy.orm import relationship
import enum
from references.approval_template.models import ApprovalTemplate
from references.enum_types.models import step_type
   
class ApprovalRoute(Base):
    __tablename__ = "approval_route"

    id = Column(Integer, primary_key = True, autoincrement = True)
    is_active = Column(Boolean, default=True)
    level = Column(Integer, nullable = False)
    type = Column(Enum(step_type), default=step_type.line)
    document_id = Column(Integer, nullable = False, index = True)
    document_type_id= Column(Integer, ForeignKey('document_type.id', ondelete = "CASCADE"), nullable = False)
    entity_iin = Column(String, ForeignKey('entity.iin', ondelete = "CASCADE"), nullable = False, index = True)
    entity = relationship("Entity")
    employee_id = Column(Integer, ForeignKey('employee.id', ondelete = "CASCADE"), nullable = False, index = True)
    employee = relationship("Employee")
    approval_template_id = Column(Integer, ForeignKey('approval_template.id', ondelete = "CASCADE"), nullable = False, index = True)
    approval_template = relationship("ApprovalTemplate")
    approval_process_id = Column(Integer, ForeignKey('approval_process.id', ondelete = "CASCADE"), nullable = False, index = True)
    approval_process = relationship("ApprovalTemplate")

    def __repr__(self) -> str:
        return self.name

Index('idx_ar_entity_document_id', ApprovalRoute.entity_iin, ApprovalRoute.document_id)
        

class ApprovalRouteOut(BaseModel):
    
    id: int
    is_active: bool
    level: int
    type: step_type
    document_id: int
    document_type_id: int
    entity_iin: str
    employee_id: int
    approval_template_id: int
    approval_process_id: int
    
    class Config:
        orm_mode = True

class ApprovalRouteIn(BaseModel):
    
    is_active: bool
    level: int
    type: step_type
    document_id: int
    document_type_id: int
    entity_iin: str
    employee_id: int
    approval_template_id: int
    approval_process_id: int
    
    class Config:
        orm_mode = True