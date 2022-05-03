from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Index, String, Integer, Boolean, Enum 
from core.db import Base
from sqlalchemy.orm import relationship
import enum
from references.approval_template.models import ApprovalTemplate
from references.enum_types.models import step_type

   
class ApprovalTemplateStep(Base):
    __tablename__ = "approval_template_step"

    id = Column(Integer, primary_key = True, autoincrement = True)
    level = Column(Integer, nullable = False)
    type = Column(Enum(step_type))
    entity_iin = Column(String, ForeignKey('entity.iin', ondelete = "CASCADE"), nullable = False, index = True)
    entity = relationship("Entity")
    employee_id = Column(Integer, ForeignKey('employee.id', ondelete = "CASCADE"), nullable = False, index = True)
    employee = relationship("Employee")
    approval_template_id = Column(Integer, ForeignKey('approval_template.id', ondelete = "CASCADE"), nullable = False, index = True)
    approval_template = relationship("ApprovalTemplate")

    def __repr__(self) -> str:
        return self.name

Index('idx_entity_at', ApprovalTemplateStep.entity_iin, ApprovalTemplateStep.approval_template_id)
        

class ApprovalTemplateStepOut(BaseModel):
    
    id: int = 0
    level: int = 0
    type: step_type = step_type.line
    entity_iin: str = '000000000000'
    employee_id: int = 0
    approval_template_id: int = 0
    
    class Config:
        orm_mode = True

class ApprovalTemplateStepIn(BaseModel):
    
    level: int = 0
    type: step_type = step_type.line
    entity_iin: str = '000000000000'
    employee_id: int = 0
    approval_template_id: int = 0

    class Config:
        orm_mode = True