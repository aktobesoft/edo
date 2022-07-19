
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date
from core.db import Base, metadata
from sqlalchemy.orm import relationship
from documents.base_document.models import Paginator
from catalogs.enum_types.models import EnumBusinessType, EnumBusinessTypeOut
from catalogs.user.models import User
from datetime import date, datetime

class Counterparty(Base):
    __tablename__ = "counterparty"

    id = Column(Integer, primary_key = True, autoincrement = True) 
    name = Column(String(150), nullable = False)
    full_name = Column(String(360), nullable=True)
    iin = Column(String(12), nullable = False, index = True, unique=True)
    address = Column(String(350))
    comment = Column(String(350))
    contact = Column(String(150))
    type_name = Column(String(50), ForeignKey('enum_business_type.name'))
    type = relationship("EnumBusinessType")

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.name, self.iin)

    def get_html_attr(self):
            return {
            'id' : {'label':'ИД', 'type': 'text', 'skip': False, 'readonly': True},
            'name' : {'label':'Наименование', 'type': 'text', 'skip': False},
            'full_name' : {'label':'Полное наименование', 'type': 'textarea', 'skip': False},
            'iin' : {'label':'ИИН', 'type': 'number', 'skip': False, 'min': '1', 'max': '999999999999', 'maxlength': '12', 'pattern': '[0-9]'},
            'type_name' : {'label':'Тип организации', 'type': 'select', 'skip': False, 'get_from_api': True},
            'address' : {'label':'Адрес', 'type': 'text', 'skip': False},
            'comment' : {'label':'Комментарий', 'type': 'textarea', 'skip': False},
            'contact' : {'label':'Руководитель', 'type': 'text', 'skip': False},
            }

class CounterpartyOut(BaseModel):
    id: int
    name: str
    full_name: str 
    iin: str
    address: str
    comment: str
    contact: str
    type_name: str
    #type: EnumBusinessTypeOut
    
    class Config:
        orm_mode = True

class CounterpartySmallOut(BaseModel):
    id: int
    name: str
    iin: str
        
    class Config:
        orm_mode = True

class CounterpartyNestedOut(BaseModel):
    id: int
    name: str
    full_name: str 
    iin: str
    address: str
    comment: str
    contact: str
    type_name: str
    type: EnumBusinessTypeOut
    
    class Config:
        orm_mode = True

class CounterpartyIn(BaseModel):
    name: str
    full_name: str 
    iin: str
    address: str
    comment: str
    contact: str
    type_name: str
    
    class Config:
        orm_mode = True

class CounterpartyListOut(BaseModel):
    info: Paginator
    result: list[CounterpartyOut]

class CounterpartyListNestedOut(BaseModel):
    info: Paginator
    result: list[CounterpartyNestedOut]

def counterparty_fill_data_from_dict(queryResult : dict):
    return {
        'id': queryResult['counterparty_id'],
        'iin': queryResult['counterparty_iin'],
        'name': queryResult['counterparty_name']
        } 