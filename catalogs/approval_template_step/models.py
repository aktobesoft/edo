from typing import Union
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Index, String, Integer, Boolean, Enum 
from core.db import Base
from sqlalchemy.orm import relationship
import enum
from catalogs.employee.models import EmployeeSmallOut
from catalogs.entity.models import EntitySmallOut
from catalogs.enum_types.models import StepType

   
class ApprovalTemplateStep(Base):
    __tablename__ = "approval_template_step"

    id = Column(Integer, primary_key = True, autoincrement = True)
    level = Column(Integer, nullable = False)
    type = Column(String, ForeignKey('step_type.name'), nullable = True)
    step_type = relationship("StepType")
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable = False, index = True)
    employee = relationship("Employee")
    approval_template_id = Column(Integer, ForeignKey('approval_template.id'), nullable = False, index = True)
    approval_template = relationship("ApprovalTemplate")
    hash = Column(String, index = True)

    def __repr__(self) -> str:
        return self.name


class _ApprovalTemplateStepOut(BaseModel):
    
    id: int = 0
    level: int = 0
    type: Union[str, None] = ''
    employee_id: int = 0
    approval_template_id: int = 0
    hash: Union[str, None] = ''
    
    class Config:
        orm_mode = True

class _ApprovalTemplateStepNestedOut(BaseModel):
    
    id: int = 0
    level: int = 0
    type: Union[str, None] = ''
    employee_id: int = 0
    employee: EmployeeSmallOut
    hash: Union[str, None] = ''
    
    class Config:
        orm_mode = True

class _ApprovalTemplateStepPUT(BaseModel):
    
    id: int = 0
    level: int = 0
    type: Union[str, None] = ''
    employee_id: int = 0
    hash: Union[str, None] = ''

    class Config:
        orm_mode = True

class _ApprovalTemplateStepPOST(BaseModel):
    
    level: int = 0
    type: Union[str, None] = ''
    employee_id: int = 0
    hash: Union[str, None] = ''

    class Config:
        orm_mode = True