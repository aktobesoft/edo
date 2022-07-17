from typing import Union
from sqlalchemy import Column, Integer, String
from core.db import Base
from pydantic import BaseModel

class EnumDocumentType(Base):
    __tablename__ = "enum_document_type"

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(150), nullable = False, unique=True)
    metadata_name = Column(String(150), nullable = True, unique=True)
    description = Column(String(350), nullable = False)

    def __repr__(self) -> str:
        return self.description

class EnumDocumentTypeOut(BaseModel): 
    
    id: Union[int, None]
    name: Union[str, None]
    description: Union[str, None]
    
    class Config:
        orm_mode = True

class EnumBusinessType(Base):
    __tablename__ = "enum_business_type"

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(150), index = True, unique=True)
    full_name = Column(String(360))

    def __repr__(self) -> str:
        return self.name

class EnumBusinessTypeOut(BaseModel):
    
    id: Union[int, None]
    name: Union[str, None]
    full_name: Union[str, None]
    
    class Config:
        orm_mode = True

class EnumStepType(Base):
    __tablename__ = 'enum_step_type'
    
    name = Column(String(150), primary_key = True)
    description = Column(String(360), nullable=True)

class EnumProcessStatusType(Base):
    __tablename__ = 'enum_process_status_type'
    
    name = Column(String(150), primary_key = True)
    description = Column(String(360), nullable=True)

class EnumRouteStatusType(Base):
    __tablename__ = 'enum_route_status_type'
    
    name = Column(String(150), primary_key = True)
    description = Column(String(360), nullable=True)

class EnumTaskStatusType(Base):
    __tablename__ = 'enum_task_status_type'
    
    name = Column(String(150), primary_key = True)
    description = Column(String(360), nullable=True)


    
    
