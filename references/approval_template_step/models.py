from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Index, String, Integer, Boolean, Enum 
from core.db import Base
from sqlalchemy.orm import relationship
import enum
from references.employee.models import EmployeeSmallOut
from references.entity.models import EntitySmallOut
from references.enum_types.models import step_type

   
class ApprovalTemplateStep(Base):
    __tablename__ = "approval_template_step"

    id = Column(Integer, primary_key = True, autoincrement = True)
    level = Column(Integer, nullable = False)
    type = Column(Enum(step_type))
    employee_id = Column(Integer, ForeignKey('employee.id', ondelete = "CASCADE"), nullable = False, index = True)
    employee = relationship("Employee")
    approval_template_id = Column(Integer, ForeignKey('approval_template.id', ondelete = "CASCADE"), nullable = False, index = True)
    approval_template = relationship("ApprovalTemplate")
    hash = Column(String, index = True)

    def __repr__(self) -> str:
        return self.name


class _ApprovalTemplateStepOut(BaseModel):
    
    id: int = 0
    level: int = 0
    type: step_type = step_type.line
    employee_id: int = 0
    approval_template_id: int = 0
    hash: str = ''
    
    class Config:
        orm_mode = True

class _ApprovalTemplateStepNestedOut(BaseModel):
    
    id: int = 0
    level: int = 0
    type: step_type = step_type.line
    employee_id: int = 0
    employee: EmployeeSmallOut
    hash: str = ''
    
    class Config:
        orm_mode = True

class _ApprovalTemplateStepPUT(BaseModel):
    
    id: int = 0
    level: int = 0
    type: step_type = step_type.line
    employee_id: int = 0
    hash: str = ''

    class Config:
        orm_mode = True

class _ApprovalTemplateStepPOST(BaseModel):
    
    level: int = 0
    type: step_type = step_type.line
    employee_id: int = 0
    hash: str = ''

    class Config:
        orm_mode = True