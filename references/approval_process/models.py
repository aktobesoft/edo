from email.policy import default
from pydantic import BaseModel
from sqlalchemy import Column, Enum, ForeignKey, String, Integer, Boolean 
from core.db import Base
from sqlalchemy.orm import relationship
from references.enum_types.models import step_type, status_type
   
class ApprovalProcess(Base):
    __tablename__ = "approval_process"

    id = Column(Integer, primary_key = True, autoincrement = True)
    is_active = Column(Boolean, default=True)
    document_id = Column(Integer, nullable = False, index = True)
    document_type_id= Column(Integer, ForeignKey('document_type.id', ondelete = "CASCADE"), nullable = False)
    entity_iin = Column(String, ForeignKey('entity.iin', ondelete = "CASCADE"), nullable = False, index = True)
    entity = relationship("Entity")
    approval_template_id = Column(Integer, ForeignKey('approval_template.id', ondelete = "CASCADE"), nullable = False, index = True)
    approval_template = relationship("ApprovalTemplate")
    status = Column(Enum(status_type), index = True, default = status_type.draft)


class ApprovalProcessOut(BaseModel):
    
    id: int
    is_active = bool
    document_id = int
    document_type_id: int
    entity_iin: str
    approval_template_id: int
    status = status_type
    
    class Config:
        orm_mode = True

class ApprovalProcessIn(BaseModel):
    
    is_active = bool
    document_id = int
    document_type_id: int
    entity_iin: str
    approval_template_id: int
    status = status_type
    
    class Config:
        orm_mode = True
