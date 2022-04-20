from enum import unique
from sqlalchemy import Column, String, Integer, Table, DateTime, Boolean, MetaData, ForeignKey, Date, event
from sqlalchemy.orm import relationship
from core.db import Base
from datetime import date, datetime
from pydantic import BaseModel, validator
from references.business_type.models import BusinessTypeOut, BusinessType
from references.document_type.models import DocumentType
from references.notes.models import Notes
from references.user.models import UserOut, User

class Entity(Base):
    __tablename__ = 'entity'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    iin = Column(String(12), nullable=False, index=True, unique=True)
    address = Column(String(350), nullable=True)
    comment = Column(String(350), nullable=True)
    director = Column(String(150), nullable=True)
    director_phone = Column(String(20), nullable=True)
    administrator = Column(String(150), nullable=True)
    administrator_phone = Column(String(20), nullable=True)
    token = Column(String(64), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    type_id = Column(Integer, ForeignKey('business_type.id', ondelete='CASCADE'), nullable=True)
    type = relationship('BusinessType')
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    user = relationship('User')

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.name, self.iin)

    def asdict(self):
        return {
        'id': self.id if self.id != None else 0, 
        'name': self.name if self.id != None else '',
        'iin': self.iin if self.id != None else '',
        'type_id': self.type_id if self.id != None else 0,
        'user_id': self.user_id if self.id != None else 0, 
        'address': self.address if self.id != None else '',
        'comment': self.comment if self.id != None else '',
        'director': self.director if self.id != None else '',
        'director_phone': self.director_phone if self.id != None else '',
        'administrator': self.administrator if self.id != None else '',
        'administrator_phone': self.administrator_phone if self.id != None else '',
        'token': self.token if self.id != None else '',
        'start_date': self.start_date if self.id != None else datetime.now(),
        'end_date': self.end_date if self.id != None else datetime.now(),
        }

    def get_html_attr(self):
        return {
        'id' : {'label':'ИД', 'type': 'text', 'skip': False, 'readonly': True},
        'name' : {'label':'Наименование', 'type': 'text', 'skip': False},
        'iin' : {'label':'ИИН', 'type': 'number', 'skip': False, 'min': '1', 'max': '999999999999', 'maxlength': '12', 'pattern': '[0-9]'},
        'type_id' : {'label':'Тип организации', 'type': 'select', 'skip': False, 'get_from_api': True},
        'user_id' : {'label':'Пользователь', 'type': 'select', 'skip': False, 'get_from_api': True},
        'start_date' : {'label':'Дата начало', 'type': 'date', 'skip': False},
        'end_date' : {'label':'Дата конец', 'type': 'date', 'skip': False},
        'address' : {'label':'Адрес', 'type': 'text', 'skip': False},
        'comment' : {'label':'Комментарий', 'type': 'textarea', 'skip': False},
        'director' : {'label':'Руководитель', 'type': 'text', 'skip': False},
        'director_phone' : {'label':'Контакты руководителя', 'type': 'text', 'skip': False},
        'administrator' : {'label':'Администратор', 'type': 'text', 'skip': False},
        'administrator_phone' : {'label':'Контакты администратора', 'type': 'text', 'skip': False},
        'token' : {'label':'Токен', 'type': 'password', 'skip': False},
        }

class EntityNestedOut(BaseModel):
    name: str
    iin: str
    address: str
    comment: str
    director: str
    director_phone: str
    administrator: str
    administrator_phone: str
    token: str
    start_date: date
    end_date: date
    type: BusinessTypeOut
    user: UserOut
    
    class Config:
        orm_mode = True

class EntityOut(BaseModel):
    id: int
    name: str
    iin: str
    address: str
    comment: str
    director: str
    director_phone: str
    administrator: str
    administrator_phone: str
    start_date: date
    end_date: date
    type_id: int
    user_id: int
    
    class Config:
        orm_mode = True

class EntitySmallOut(BaseModel):
    id: int
    name: str
    iin: str

class EntityIn(BaseModel):
    name: str
    iin: str
    address: str
    comment: str
    director: str
    director_phone: str
    administrator: str
    administrator_phone: str
    start_date: date
    end_date: date
    type_id: int
    user_id: int

    class Config:
        orm_mode = True

    @validator('iin')
    def iin_must_contain_only_digits(cls, v):
        if not v.isdigit():
            raise ValueError('must contain only digits')
        return v.title()

def entity_fillDataFromDict(queryResult : dict):
    return {
        'id': queryResult['entity_id'],
        'iin': queryResult['entity_iin'],
        'name': queryResult['entity_name']
        } 

@event.listens_for(Table, 'before_insert')
def do_stuff(mapper, connect, target):
    # target is an instance of Table
    target.value = ...


