from catalogs.employee.models import Employee
from catalogs.entity.models import Entity
from catalogs.user.models import User
from core.db import database
from sqlalchemy import delete, func, select, insert, update
from sqlalchemy import exc
from pydantic import BaseModel, ValidationError, validator
import asyncpg
from auth.user_auth import get_password_hash 

async def post_user(newUser : dict):
    if 'hashed_password' in newUser and newUser['hashed_password'] != '' and newUser['hashed_password'] != None:
        query = insert(User).values(
                        name = newUser['name'], 
                        email = newUser['email'],
                        entity_iin = newUser['entity_iin'], 
                        employee_id = newUser['employee_id'], 
                        is_active = newUser['is_active'],
                        is_company = newUser['is_company'],
                        hashed_password = get_password_hash(newUser['hashed_password']))
    else:
        query = insert(User).values(
                        name = newUser['name'], 
                        email = newUser['email'],
                        entity_iin = newUser['entity_iin'], 
                        employee_id = newUser['employee_id'], 
                        is_active = newUser['is_active'],
                        is_company = newUser['is_company'])

    return await database.execute(query)

async def get_user_count():
    query = select(func.count(User.id))
    return await database.execute(query)

async def get_user_by_id(user_id: int):
    query = select(User.id, 
                    User.name, 
                    User.email, 
                    User.is_active, 
                    User.is_company,
                    User.employee_id,
                    User.entity_iin,
                    Employee.name.label('employee_name'),
                    Entity.name.label('entity_name')).\
                    join(Employee, User.employee_id == Employee.id, isouter=True).\
                    join(Entity, User.entity_iin == Entity.iin, isouter=True).\
                    where(User.id == user_id)
    resultUser = await database.fetch_one(query)
    return resultUser 
    
async def get_user_list(limit: int = 100, skip: int = 0, **kwargs):

    query = select(User.id, 
                    User.name, 
                    User.email, 
                    User.is_active, 
                    User.is_company,
                    User.employee_id,
                    User.entity_iin,
                    Employee.name.label('employee_name'),
                    Entity.name.label('entity_name')).\
                    join(Employee, User.employee_id == Employee.id, isouter=True).\
                    join(Entity, User.entity_iin == Entity.iin, isouter=True).\
                    where(User.is_active)

    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def delete_user_by_id(user_id: int):
    queryUser = delete(User).where(User.id == user_id)
    resultUser = await database.execute(queryUser)
    return resultUser

async def update_user(newUser : dict, user_id: int):
    print(newUser)
    if 'hashed_password' in newUser and newUser['hashed_password'] != '' and newUser['hashed_password'] != None:
        query = update(User).values(
                    name = newUser['name'], 
                    email = newUser['email'], 
                    entity_iin = newUser['entity_iin'], 
                    employee_id = newUser['employee_id'],
                    is_active = newUser['is_active'],
                    hashed_password = get_password_hash(newUser['hashed_password']),
                    is_company = newUser['is_company']).\
                        where(User.id == user_id)
    else:
        query = update(User).values(
                    name = newUser['name'], 
                    email = newUser['email'],
                    entity_iin = newUser['entity_iin'], 
                    employee_id = newUser['employee_id'], 
                    is_active = newUser['is_active'],
                    is_company = newUser['is_company']).\
                        where(User.id == user_id)
        
    return await database.execute(query)






    