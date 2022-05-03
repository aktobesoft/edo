from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean 
from core.db import Base
   
class BusinessType(Base):
    __tablename__ = "business_type"

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(150), index = True, unique=True)
    full_name = Column(String(360))

    def __repr__(self) -> str:
        return self.name
        

class BusinessTypeOut(BaseModel):
    
    id: int
    name: str
    full_name: str
    
    class Config:
        orm_mode = True

class BusinessTypeIn(BaseModel):
    
    name: str
    full_name: str
    
    class Config:
        orm_mode = True

def business_type_fillDataFromDict(queryResult : dict):
    return {
        'id': queryResult['business_type_id'],
        'name': queryResult['business_type_name'],
        'full_name': queryResult['business_type_full_name'] 
        } 
