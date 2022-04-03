from pydantic import BaseModel
from typing import List, Any
from datetime import date

class NotesOut(BaseModel):
    id: int
    text: str
    completed: bool

class UserOut(BaseModel):
    id: int
    email: str
    is_active: bool

    class Config:
        orm_mode = True

class UserOptionsOut(BaseModel):
    
    value: int
    text: str
    
    class Config:
        orm_mode = True


class BusinessTypeOut(BaseModel):
    
    id: int
    name: str
    full_name: str
    
    class Config:
        orm_mode = True

class BusinessTypeOptionsOut(BaseModel):
    
    value: int
    text: str
    
    class Config:
        orm_mode = True

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

class EntityLabel():
    id = {'label':'ИД', 'type': 'text', 'skip': False}
    name = {'label':'Наименование', 'type': 'text', 'skip': False}
    iin = {'label':'ИИН', 'type': 'text', 'skip': False}
    address = {'label':'Адрес', 'type': 'text', 'skip': False}
    comment = {'label':'Комментарий', 'type': 'textarea', 'skip': False}
    director = {'label':'Руководитель', 'type': 'text', 'skip': False}
    director_phone = {'label':'Контакты руководителя', 'type': 'text', 'skip': False}
    administrator = {'label':'Администратор', 'type': 'text', 'skip': False}
    administrator_phone = {'label':'Контакты администратора', 'type': 'text', 'skip': False}
    token = {'label':'Токен', 'type': 'text', 'skip': False}
    startDate = {'label':'Дата начало', 'type': 'date', 'skip': False}
    endDate = {'label':'Дата конец', 'type': 'date', 'skip': False}
    type_id = {'label':'Тип документа', 'type': 'select', 'skip': False, 'get_from_api': True}
    user_id = {'label':'Пользователь', 'type': 'select', 'skip': False, 'get_from_api': True}
    #user = {'label':'Пользователь', 'type': 'select', 'skip': False}

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