from sqlalchemy import select, insert, update, delete
from core.db import database
import asyncpg
from datetime import date, datetime
from common_module.urls_module import correct_date

from references.user.models import User
from references.entity.models import Entity
from references.employee.models import Employee, EmployeeIn, EmployeeOut

async def get_employee_by_id(employee_id: int):
    query = select(Employee).where(Employee.id == employee_id)
    result = await database.fetch_one(query)
    return result

async def delete_employee_by_id(employee_id: int):
    query = delete(Employee).where(Employee.id == employee_id)
    result = await database.execute(query)
    return result

async def get_employee_list(limit: int = 100, 
                        skip: int = 0,
                        **kwargs)->list[Employee]:
    query = select(Employee.id, 
                Employee.name, 
                Employee.email, 
                Employee.date_of_birth, 
                Employee.description, 
                Employee.entity_id, 
                Employee.user_id,
                User.email.label("user_email"), 
                User.name.label("user_name")).join(
                Entity, Employee.entity_id == Entity.id).join(
                User, Employee.user_id == User.id).order_by(
                    Employee.id).limit(limit).offset(skip)
   
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def post_employee(employeeInstance : dict):
    employeeInstance["date_of_birth"] = correct_date(employeeInstance["date_of_birth"])

    query = insert(Employee).values(
                name = employeeInstance["name"], 
                email = employeeInstance["email"], 
                date_of_birth = employeeInstance["date_of_birth"],
                description = employeeInstance["description"], 
                entity_id = int(employeeInstance["entity_id"]),
                user_id = int(employeeInstance["user_id"])
                )
    try:
        newEmloyeeId = await database.execute(query)
    except asyncpg.exceptions.ForeignKeyViolationError as e:
        raise ValueError('Не уникальный email')
    
    return {**employeeInstance, 'id': newEmloyeeId}

async def update_employee(employeeInstance : dict):
    employeeInstance['date_of_birth'] = correct_date(employeeInstance['date_of_birth'])
    
    query = update(Employee).values(name = employeeInstance["name"], 
                email = employeeInstance["email"], 
                date_of_birth = employeeInstance['date_of_birth'],
                description = employeeInstance["description"], 
                entity_id = int(employeeInstance["entity_id"]),
                user_id = int(employeeInstance["user_id"])).where(Employee.id == int(employeeInstance['id']))
    print(query)
    result = await database.execute(query)
    return {**employeeInstance}
