from pydantic import BaseModel
from schemas.user import UserOut
from typing import List, Any
from datetime import date

class EntityUserOut(BaseModel):
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
    type_id: int
    user: UserOut
    
    class Config:
        orm_mode = True

class EntityLabel():
    id = {'label':'ИД', 'type': 'text'}
    name = {'label':'Наименование', 'type': 'text'}
    iin = {'label':'ИИН', 'type': 'text'}
    address = {'label':'Адрес', 'type': 'text'}
    comment = {'label':'Комментарий', 'type': 'text'}
    director = {'label':'Руководитель', 'type': 'text'}
    director_phone = {'label':'Контакты руководителя', 'type': 'text'}
    administrator = {'label':'Администратор', 'type': 'text'}
    administrator_phone = {'label':'Контакты администратора', 'type': 'text'}
    token = {'label':'Токен', 'type': 'text'}
    startDate = {'label':'Дата начало', 'type': 'text'}
    endDate = {'label':'Дата конец', 'type': 'text'}
    type_id = {'label':'Тип документа', 'type': 'select'}
    user_id = {'label':'Пользователь', 'type': 'select'}

class EntityOut(BaseModel):
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