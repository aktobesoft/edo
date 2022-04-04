from enum import unique
from sqlalchemy import Column, String, Integer, Table, DateTime, Boolean, MetaData, ForeignKey, Date, event
from sqlalchemy.orm import relationship
from core.db import Base, metadata
from datetime import date, datetime
from pydantic import BaseModel, validator
from .business_type import BusinessTypeOut, BusinessType
from .document_type import DocumentType
from .notes import Notes
from .user import UserOut, User

class Entity(Base):
    __tablename__ = "entity"
    
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
    startDate = Column(Date, nullable=True)
    endDate = Column(Date, nullable=True)
    type_id = Column(Integer, ForeignKey('business_type.id', ondelete="CASCADE"), nullable=True)
    type = relationship("BusinessType")
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    user = relationship("User")

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
        'startDate': self.startDate if self.id != None else datetime.now(),
        'endDate': self.endDate if self.id != None else datetime.now(),
        }

    def get_html_attr(self):
        return {
        'id' : {'label':'ИД', 'type': 'text', 'skip': False, 'readonly': 'readonly'},
        'name' : {'label':'Наименование', 'type': 'text', 'skip': False, 'readonly': ''},
        'iin' : {'label':'ИИН', 'type': 'text', 'skip': False, 'readonly': ''},
        'address' : {'label':'Адрес', 'type': 'text', 'skip': False, 'readonly': ''},
        'comment' : {'label':'Комментарий', 'type': 'textarea', 'skip': False, 'readonly': ''},
        'director' : {'label':'Руководитель', 'type': 'text', 'skip': False, 'readonly': ''},
        'director_phone' : {'label':'Контакты руководителя', 'type': 'text', 'skip': False, 'readonly': ''},
        'administrator' : {'label':'Администратор', 'type': 'text', 'skip': False, 'readonly': ''},
        'administrator_phone' : {'label':'Контакты администратора', 'type': 'text', 'skip': False, 'readonly': ''},
        'token' : {'label':'Токен', 'type': 'password', 'skip': False, 'readonly': ''},
        'startDate' : {'label':'Дата начало', 'type': 'date', 'skip': False, 'readonly': ''},
        'endDate' : {'label':'Дата конец', 'type': 'date', 'skip': False, 'readonly': ''},
        'type_id' : {'label':'Тип организации', 'type': 'select', 'skip': False, 'get_from_api': True, 'readonly': ''},
        'user_id' : {'label':'Пользователь', 'type': 'select', 'skip': False, 'get_from_api': True, 'readonly': ''},
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
    startDate: date
    endDate: date
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
    startDate: date
    endDate: date
    type_id: int
    user_id: int
    
    class Config:
        orm_mode = True

class EntityIn(BaseModel):
    name: str
    iin: str
    address: str
    comment: str
    director: str
    director_phone: str
    administrator: str
    administrator_phone: str
    startDate: date
    endDate: date
    type_id: int
    user_id: int

    class Config:
        orm_mode = True

    @validator('iin')
    def iin_must_contain_only_digits(cls, v):
        if not v.isdigit():
            raise ValueError('must contain only digits')
        return v.title()

@event.listens_for(Table, 'before_insert')
def do_stuff(mapper, connect, target):
    # target is an instance of Table
    target.value = ...


