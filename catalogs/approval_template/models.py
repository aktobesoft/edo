from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Index, String, Integer, Boolean 
from core.db import Base
from sqlalchemy.orm import relationship
from catalogs.approval_template_step.models import _ApprovalTemplateStepPOST, _ApprovalTemplateStepPUT, _ApprovalTemplateStepNestedOut, _ApprovalTemplateStepOut

from catalogs.enum_types.models import EnumDocumentTypeOut
from catalogs.entity.models import EntitySmallOut
   
class ApprovalTemplate(Base):
    __tablename__ = "approval_template"

    id = Column(Integer, primary_key = True, autoincrement = True)
    enum_document_type_id = Column(Integer, ForeignKey('enum_document_type.id'), nullable = False)
    enum_document_type = relationship("EnumDocumentType")
    name = Column(String(150))
    entity_iin = Column(String, ForeignKey('entity.iin'), nullable = False, index = True)
    entity = relationship("Entity")

    def __repr__(self) -> str:
        return self.name

Index('index_at_entity_enum_document_type', ApprovalTemplate.entity_iin, ApprovalTemplate.enum_document_type_id)

class ApprovalTemplateOut(BaseModel):
    
    id: int
    enum_document_type_id: int
    name: str
    entity_iin: str
    
    class Config:
        orm_mode = True

class ApprovalTemplateStepOut(BaseModel):
    
    id: int
    enum_document_type_id: int
    name: str
    entity_iin: str
    steps: list[_ApprovalTemplateStepOut]
    
    class Config:
        orm_mode = True


class ApprovalTemplateNestedOut(BaseModel):
    
    id: int
    enum_document_type_id: int
    enum_document_type: EnumDocumentTypeOut
    name: str
    entity_iin: str
    entity: EntitySmallOut
    
    class Config:
        orm_mode = True

class ApprovalTemplateStepsNestedOut(BaseModel):
    
    id: int = 0
    enum_document_type_id: int = 0
    enum_document_type: EnumDocumentTypeOut
    name: str = 'Шаблон'
    entity_iin: str = '000123456789'
    entity: EntitySmallOut
    steps: list[_ApprovalTemplateStepNestedOut]
    
    class Config:
        orm_mode = True

class ApprovalTemplateIn(BaseModel):
    
    enum_document_type_id: int = '0'
    name: str = 'Шаблон документа'
    entity_iin: str = '000123456789'
    
    class Config:
        orm_mode = True

class ApprovalTemplatePOST(BaseModel):
    
    enum_document_type_id: int = '0'
    name: str = 'Шаблон документа'
    entity_iin: str = '000123456789'
    steps: list[_ApprovalTemplateStepPOST]
    
    class Config:
        orm_mode = True

class ApprovalTemplatePUT(BaseModel):
    
    id: int = 0
    enum_document_type_id: int = '0'
    name: str = 'Шаблон документа'
    entity_iin: str = '000123456789'
    steps: list[_ApprovalTemplateStepPUT]
    
    class Config:
        orm_mode = True

def approval_template_fill_data_from_dict(queryResult : dict):
    return {
        'id': queryResult['approval_template_id'],
        'enum_document_type_id': queryResult['enum_document_type_id'],
        'name': queryResult['approval_template_name']
        } 


