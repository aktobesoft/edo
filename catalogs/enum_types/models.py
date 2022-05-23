from sqlalchemy import Column, String
from core.db import Base

class StepType(Base):
    __tablename__ = 'step_type'
    
    name = Column(String(150), primary_key = True)
    description = Column(String(360), nullable=True)

class ProcessStatusType(Base):
    __tablename__ = 'process_status_type'
    
    name = Column(String(150), primary_key = True)
    description = Column(String(360), nullable=True)

class RouteStatusType(Base):
    __tablename__ = 'route_status_type'
    
    name = Column(String(150), primary_key = True)
    description = Column(String(360), nullable=True)
    
