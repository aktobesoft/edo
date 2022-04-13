from datetime import date
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from core.db import Base
from references.business_type.models import BusinessTypeOut
from references.entity.models import Entity

class Employee(Base):
    __tablename__ = "employee"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    date_of_birth = Column(Date, nullable=True)
    name = Column(String(150), nullable=False)
    description = Column(String(350), nullable=True)
    entity_id = Column(Integer, ForeignKey('entity.id', ondelete="CASCADE"), nullable=False)
    entity = relationship("Entity")
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    user = relationship("User")

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.name, self.email)

    def asdict(self):
        return {
        'id': self.id if self.id != None else 0, 
        'name': self.name if self.id != None else '',
        'email': self.email if self.id != None else '',
        'entity_id': self.entity_id if self.id != None else 0,
        'user_id': self.user_id if self.id != None else 0, 
        'description': self.description if self.id != None else '',
        'date_of_birth': self.start_date if self.id != None else '',
        }

    def get_html_attr(self):
        return {
        'id' : {'label':'ИД', 'type': 'text', 'skip': False, 'readonly': True},
        'name' : {'label':'Наименование', 'type': 'text', 'skip': False},
        'email' : {'label':'Email', 'type': 'email', 'skip': False},
        'entity_id' : {'label':'Организации', 'type': 'select', 'skip': False, 'get_from_api': True},
        'user_id' : {'label':'Пользователь', 'type': 'select', 'skip': False, 'get_from_api': True},
        'date_of_birth' : {'label':'День рождения', 'type': 'date', 'skip': False},
        'description' : {'label':'Контакты руководителя', 'type': 'text', 'skip': False},
        }

class EmployeeOut(BaseModel):
    id: int
    name: str
    email: str
    entity_id: int
    user_id: int
    description: str
    date_of_birth: date
    
    class Config:
        orm_mode = True

class EmployeeIn(BaseModel):
   
    name: str
    email: str
    entity_id: int
    user_id: int
    description: str
    date_of_birth: date
    
    class Config:
        orm_mode = True