
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date
from core.db import Base, metadata
from sqlalchemy.orm import relationship
from references.business_type.models import BusinessType, BusinessTypeOut
from references.user.models import User
from datetime import date, datetime

class Counterparty(Base):
    __tablename__ = "сounterparty"

    id = Column(Integer, primary_key=True, autoincrement=True) 
    name = Column(String(150), nullable=False)
    iin = Column(String(12), nullable=False, index=True, unique=True)
    address = Column(String(350))
    comment = Column(String(350))
    contact = Column(String(150))
    type_id = Column(Integer, ForeignKey('business_type.id'))
    type = relationship("BusinessType")

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.name, self.iin)

class CounterpartyOut(BaseModel):
    id: int
    name: str
    iin: str
    address: str
    comment: str
    contact: str
    type_id: int
    #type: BusinessTypeOut
    
    class Config:
        orm_mode = True

class CounterpartyIn(BaseModel):
    name: str
    iin: str
    address: str
    comment: str
    contact: str
    type_id: int
    
    class Config:
        orm_mode = True
