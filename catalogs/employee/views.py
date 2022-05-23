from sqlalchemy import func, select, insert, update, delete
from core.db import database
import asyncpg
from datetime import date, datetime
from common_module.urls_module import correct_datetime

from catalogs.user.models import User, user_fillDataFromDict
from catalogs.entity.models import Entity, entity_fillDataFromDict
from catalogs.employee.models import Employee, EmployeeIn, EmployeeOut

async def get_employee_by_id(employee_id: int):
    query = select(Employee).where(Employee.id == employee_id)
    result = await database.fetch_one(query)
    return result

async def delete_employee_by_id(employee_id: int):
    query = delete(Employee).where(Employee.id == employee_id)
    result = await database.execute(query)
    return result

async def get_employee_count():
    query = select(func.count(Employee.id))
    return await database.execute(query)

async def get_employee_list(limit: int = 100, skip: int = 0, **kwargs)->list[Employee]:

    if(kwargs['nested']):
        return await get_employee_nested_list(limit, skip, **kwargs)
    if('optional' in kwargs and kwargs['optional']):
        return await get_employee_options_list(limit, skip, **kwargs)    
                        
    query = select(Employee.id, 
                Employee.name, 
                Employee.email, 
                Employee.date_of_birth, 
                Employee.description, 
                Employee.entity_iin, 
                Employee.user_id).\
                    order_by(
                    Employee.id).limit(limit).offset(skip)
   
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def get_employee_nested_list(limit: int = 100, skip: int = 0, **kwargs):
                        
    query = select(Employee.id, 
                Employee.name, 
                Employee.email, 
                Employee.date_of_birth, 
                Employee.description, 
                Employee.entity_iin.label("entity_iin"), 
                Employee.user_id,
                User.email.label("user_email"), 
                User.name.label("user_name"),
                User.is_active.label("user_is_active"),
                User.is_company.label("user_is_company"),
                Entity.name.label("entity_name"),
                Entity.id.label("entity_id")).\
                    join(Entity, Employee.entity_iin == Entity.iin, isouter=True).\
                    join(User, Employee.user_id == User.id, isouter=True).\
                    order_by(Employee.id).limit(limit).offset(skip)
   
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['user'] = user_fillDataFromDict(recordDict)
        recordDict['entity'] = entity_fillDataFromDict(recordDict)
        listValue.append(recordDict)
    return listValue

async def get_employee_options_list(limit: int = 100, skip: int = 0, **kwargs)->list[Employee]:

    query = select(Employee.id.label('value'), 
                Employee.name, 
                Employee.email).order_by(
                    Employee.id).limit(limit).offset(skip)
   
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = {}
        recordDict['value'] = rec['value']
        recordDict['text'] = '{0} ({1})'.format(rec['name'],rec['email'])
        listValue.append(recordDict)
    return listValue

async def post_employee(employeeInstance : dict):
    employeeInstance["date_of_birth"] = correct_datetime(employeeInstance["date_of_birth"])

    query = insert(Employee).values(
                name = employeeInstance["name"], 
                email = employeeInstance["email"], 
                date_of_birth = employeeInstance["date_of_birth"],
                description = employeeInstance["description"], 
                entity_iin = employeeInstance["entity_iin"],
                user_id = int(employeeInstance["user_id"])
                )
    try:
        newEmloyeeId = await database.execute(query)
    except asyncpg.exceptions.ForeignKeyViolationError as e:
        raise ValueError('Не уникальный email')
    
    return {**employeeInstance, 'id': newEmloyeeId}

async def update_employee(employeeInstance : dict, employee_id: int):
    employeeInstance['date_of_birth'] = correct_datetime(employeeInstance['date_of_birth'])
    
    query = update(Employee).values(name = employeeInstance["name"], 
                email = employeeInstance["email"], 
                date_of_birth = employeeInstance['date_of_birth'],
                description = employeeInstance["description"], 
                entity_iin = employeeInstance["entity_iin"],
                user_id = int(employeeInstance["user_id"])).where(Employee.id == employee_id)
    result = await database.execute(query)
    return {**employeeInstance}
