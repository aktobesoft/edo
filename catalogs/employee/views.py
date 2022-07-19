from fastapi import HTTPException
from sqlalchemy import func, select, insert, update, delete
from core.db import database
import asyncpg
from common_module.urls_module import correct_datetime, is_need_filter

from catalogs.entity.models import Entity, entity_fill_data_from_dict
from catalogs.employee.models import Employee

async def get_employee_by_id(employee_id: int, **kwargs):
    query = select(Employee).where(Employee.id == employee_id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(Employee.entity_iin.in_(kwargs['entity_iin_list']))
    result = await database.fetch_one(query)
    return result

async def delete_employee_by_id(employee_id: int, **kwargs):
    query = delete(Employee).where(Employee.id == employee_id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(Employee.entity_iin.in_(kwargs['entity_iin_list']))
    result = await database.execute(query)
    return result

async def get_employee_count(**kwargs):
    query = select(func.count(Employee.id))
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(Employee.entity_iin.in_(kwargs['entity_iin_list']))
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
                Employee.entity_iin).\
                    order_by(
                    Employee.id).limit(limit).offset(skip)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(Employee.entity_iin.in_(kwargs['entity_iin_list']))
   
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
                Entity.name.label("entity_name"),
                Entity.id.label("entity_id")).\
                    join(Entity, Employee.entity_iin == Entity.iin, isouter=True).\
                    order_by(Employee.id).limit(limit).offset(skip)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(Employee.entity_iin.in_(kwargs['entity_iin_list']))
   
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['entity'] = entity_fill_data_from_dict(recordDict)
        listValue.append(recordDict)
    return listValue

async def get_employee_options_list(limit: int = 100, skip: int = 0, **kwargs)->list[Employee]:

    query = select(Employee.id.label('value'), 
                Employee.name, 
                Employee.email).order_by(
                    Employee.id).limit(limit).offset(skip)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(Employee.entity_iin.in_(kwargs['entity_iin_list']))
   
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = {}
        recordDict['value'] = rec['value']
        recordDict['text'] = '{0} ({1})'.format(rec['name'],rec['email'])
        listValue.append(recordDict)
    return listValue

async def post_employee(employeeInstance : dict, **kwargs):
    # RLS
    if(is_need_filter('entity_iin_list', kwargs) and employeeInstance["entity_iin"] not in kwargs['entity_iin_list']):
        raise HTTPException(status_code=403, detail="Forbidden")

    employeeInstance["date_of_birth"] = correct_datetime(employeeInstance["date_of_birth"])

    query = insert(Employee).values(
                name = employeeInstance["name"], 
                email = employeeInstance["email"], 
                date_of_birth = employeeInstance["date_of_birth"],
                description = employeeInstance["description"], 
                entity_iin = employeeInstance["entity_iin"] )
    try:
        newEmloyeeId = await database.execute(query)
    except asyncpg.exceptions.ForeignKeyViolationError as e:
        raise ValueError('Не уникальный email')
    
    return {**employeeInstance, 'id': newEmloyeeId}

async def update_employee(employeeInstance : dict, employee_id: int, **kwargs):
    employeeInstance['date_of_birth'] = correct_datetime(employeeInstance['date_of_birth'])
    
    query = update(Employee).values(name = employeeInstance["name"], 
                email = employeeInstance["email"], 
                date_of_birth = employeeInstance['date_of_birth'],
                description = employeeInstance["description"], 
                entity_iin = employeeInstance["entity_iin"]).\
                where(Employee.id == employee_id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(Employee.entity_iin.in_(kwargs['entity_iin_list']))

    result = await database.execute(query)
    return {**employeeInstance}
