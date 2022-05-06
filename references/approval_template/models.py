from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean 
from core.db import Base
from sqlalchemy.orm import relationship
from references.approval_template_step.models import _ApprovalTemplateStepIn, _ApprovalTemplateStepNestedOut

from references.document_type.models import DocumentTypeOut
from references.entity.models import EntitySmallOut
   
class ApprovalTemplate(Base):
    __tablename__ = "approval_template"

    id = Column(Integer, primary_key = True, autoincrement = True)
    document_type_id = Column(Integer, ForeignKey('document_type.id', ondelete = "CASCADE"), nullable = False)
    document_type = relationship("DocumentType")
    name = Column(String(150), unique=True)
    entity_iin = Column(String, ForeignKey('entity.iin', ondelete = "CASCADE"), nullable = False, index = True)
    entity = relationship("Entity")

    def __repr__(self) -> str:
        return self.name
        

class ApprovalTemplateOut(BaseModel):
    
    id: int
    document_type_id: int
    name: str
    entity_iin: str
    
    class Config:
        orm_mode = True

class ApprovalTemplateNestedOut(BaseModel):
    
    id: int
    document_type_id: int
    document_type: DocumentTypeOut
    name: str
    entity_iin: str
    entity: EntitySmallOut
    
    class Config:
        orm_mode = True

class ApprovalTemplateStepsNestedOut(BaseModel):
    
    id: int = 0
    document_type_id: int = 0
    document_type: DocumentTypeOut
    name: str = 'Шаблон'
    entity_iin: str = '000123456789'
    entity: EntitySmallOut
    steps: list[_ApprovalTemplateStepNestedOut]
    
    class Config:
        orm_mode = True

class ApprovalTemplateIn(BaseModel):
    
    document_type_id: int = '0'
    name: str = 'Шаблон документа'
    entity_iin: str = '000123456789'
    
    class Config:
        orm_mode = True

class ApprovalTemplatePOST(BaseModel):
    
    document_type_id: int = '0'
    name: str = 'Шаблон документа'
    entity_iin: str = '000123456789'
    steps: list[_ApprovalTemplateStepIn]
    
    class Config:
        orm_mode = True

class ApprovalTemplatePUT(BaseModel):
    
    document_type_id: int = '0'
    name: str = 'Шаблон документа'
    entity_iin: str = '000123456789'
    steps: list[_ApprovalTemplateStepIn]
    
    class Config:
        orm_mode = True


