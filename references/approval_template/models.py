from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Index, String, Integer, Boolean 
from core.db import Base
from sqlalchemy.orm import relationship
from references.approval_template_step.models import _ApprovalTemplateStepPOST, _ApprovalTemplateStepPUT, _ApprovalTemplateStepNestedOut, _ApprovalTemplateStepOut

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

    def asdict(self):
        return {
        'id': self.id if self.id != None else 0, 
        'document_type_id': self.document_type_id if self.document_type_id != None else '',
        'name': self.name if self.name != None else '',
        'entity_iin': self.entity_iin if self.id != None else 0,
        'steps': []
        }
        
Index('index_at_entity_document_type', ApprovalTemplate.entity_iin, ApprovalTemplate.document_type_id)

class ApprovalTemplateOut(BaseModel):
    
    id: int
    document_type_id: int
    name: str
    entity_iin: str
    
    class Config:
        orm_mode = True

class ApprovalTemplateStepOut(BaseModel):
    
    id: int
    document_type_id: int
    name: str
    entity_iin: str
    steps: list[_ApprovalTemplateStepOut]
    
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
    steps: list[_ApprovalTemplateStepPOST]
    
    class Config:
        orm_mode = True

class ApprovalTemplatePUT(BaseModel):
    
    id: int = 0
    document_type_id: int = '0'
    name: str = 'Шаблон документа'
    entity_iin: str = '000123456789'
    steps: list[_ApprovalTemplateStepPUT]
    
    class Config:
        orm_mode = True


