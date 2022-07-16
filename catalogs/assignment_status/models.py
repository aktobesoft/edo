from datetime import datetime
from typing import Literal, Union
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Index, String, Integer, Boolean, DateTime
from core.db import Base
from sqlalchemy.orm import relationship
   
class AssignmentStatus(Base):
    __tablename__ = "assignment_status"

    id = Column(Integer, primary_key = True, autoincrement = True)
    is_active = Column(Boolean, default=True)
    status = Column(String, ForeignKey('enum_assignment_status_type.name'), nullable = True)
    document_id = Column(Integer, nullable = False, index = True)
    enum_document_type_id= Column(Integer, ForeignKey('enum_document_type.id'), nullable = False)
    date = Column(DateTime(timezone=True), nullable = True, default=datetime.utcnow)
    comment = Column(String(350), nullable = True,)
    entity_iin = Column(String, ForeignKey('entity.iin'), nullable = False, index = True)
    entity = relationship("Entity")
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False, index = True)
    user = relationship("User")

    def __repr__(self) -> str:
        return self.name

class AssignmentStatusOut(BaseModel):
    
    id: int
    is_active: bool
    status: Union[str, None]
    document_id: int
    enum_document_type_id: int
    entity_iin: str
    user_id: int
    date: Union[datetime, None]
    
    class Config:
        orm_mode = True

class AssignmentStatusPUT(BaseModel):
    
    id: int
    is_active: bool
    status: Literal['в работе', 'выполнено', 'отложено', 'в ожидании', 'не выполнено', 'переназначено', 'новый']
    document_id: int
    enum_document_type_id: int
    entity_iin: str
    user_id: int
    comment: str
    
    class Config:
        orm_mode = True

class AssignmentStatusPOST(BaseModel):
    
    is_active: bool
    status: Literal['в работе', 'выполнено', 'отложено', 'в ожидании', 'не выполнено', 'переназначено', 'новый']
    document_id: int
    enum_document_type_id: int
    entity_iin: str
    user_id: int
    comment: str
    
    class Config:
        orm_mode = True