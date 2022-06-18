from datetime import datetime
from typing import Literal, Union
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Index, String, Integer, Boolean, DateTime
from core.db import Base
from sqlalchemy.orm import relationship
   
class ApprovalStatus(Base):
    __tablename__ = "approval_status"

    id = Column(Integer, primary_key = True, autoincrement = True)
    is_active = Column(Boolean, default=True)
    status = Column(String, ForeignKey('route_status_type.name'), nullable = True)
    route_status_type = relationship("RouteStatusType")
    document_id = Column(Integer, nullable = False, index = True)
    document_type_id= Column(Integer, ForeignKey('document_type.id'), nullable = False)
    date = Column(DateTime(timezone=True), nullable = True, default=datetime.utcnow)
    comment = Column(String(350), nullable = True,)
    entity_iin = Column(String, ForeignKey('entity.iin'), nullable = False, index = True)
    entity = relationship("Entity")
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False, index = True)
    user = relationship("User")
    approval_route_id = Column(Integer, ForeignKey('approval_route.id'), nullable = False, index = True)
    approval_route = relationship("ApprovalRoute")

    def __repr__(self) -> str:
        return self.name

Index('idx_as_approval_route_id_user_id', ApprovalStatus.approval_route_id, ApprovalStatus.user_id)
        

class ApprovalStatusOut(BaseModel):
    
    id: int
    is_active: bool
    status: Union[str, None]
    document_id: int
    document_type_id: int
    entity_iin: str
    user_id: int
    date: Union[datetime, None]
    approval_route_id: int
    
    class Config:
        orm_mode = True

class ApprovalStatusPUT(BaseModel):
    
    id: int
    is_active: bool
    status: Literal['согласован', 'отклонен']
    document_id: int
    document_type_id: int
    entity_iin: str
    user_id: int
    approval_route_id: int
    comment: str
    
    class Config:
        orm_mode = True

class ApprovalStatusPOST(BaseModel):
    
    is_active: bool
    status: Literal['согласован', 'отклонен']
    document_id: int
    document_type_id: int
    entity_iin: str
    user_id: int
    approval_route_id: int
    comment: str
    
    class Config:
        orm_mode = True