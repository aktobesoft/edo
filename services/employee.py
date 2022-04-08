from lib2to3.pgen2 import token
from typing import List

from databases import Database
from models.entity import Entity, EntityIn, EntityOut
from models.employee import Employee, EmployeeIn, EmployeeOut
from models.business_type import BusinessType
from sqlalchemy import select, insert, update, delete
from core.db import database
import asyncpg
from datetime import date, datetime

from models.user import User

async def get_employee_by_id(employee_id: int):
    queryEmployee = select(Employee).where(Employee.id == employee_id)
    resultEmployee = await database.fetch_one(queryEmployee)
    return resultEmployee

async def delete_employee_by_id(employee_id: int):
    queryEmployee = delete(Employee).where(Employee.id == employee_id)
    resultEmployee = await database.execute(queryEmployee)
    print(resultEmployee)
    return resultEmployee

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

async def post_employee(employeeInstance : EmployeeOut):
    newEmployee = dict(employeeInstance)

    if type(newEmployee["date_of_birth"]) is date:
        date_of_birth = newEmployee["date_of_birth"]
    elif type(newEmployee["date_of_birth"]) is str and newEmployee["date_of_birth"] != 'None' or newEmployee["date_of_birth"] != '':  
        date_of_birth = datetime.now()

    query = insert(Employee).values(
                name = newEmployee["name"], 
                email = newEmployee["email"], 
                date_of_birth = date_of_birth,
                description = newEmployee["description"], 
                entity_id = int(newEmployee["entity_id"]),
                user_id = int(newEmployee["user_id"])
                )
    print(query)
    try:
        newEmployee = await database.fetch_one(query)
    except asyncpg.exceptions.ForeignKeyViolationError as e:
        raise ValueError('Не уникальный email')
    
    if newEmployee != None:
        query = select(Employee).where(Employee.id == newEmployee.id)
        record = await database.fetch_one(query)
        if (record != None):
            return dict(record)
    return EmployeeIn

async def update_employee(employee_id: int, employeeInstance: dict):

    queryEmployee = select(Employee).where(Employee.id == employee_id)
    resultEmployee = await database.fetch_one(queryEmployee)

    if type(employeeInstance["date_of_birth"]) is date:
        date_of_birth = employeeInstance["date_of_birth"]
    elif type(employeeInstance["date_of_birth"]) is str and employeeInstance["date_of_birth"] != 'None' or employeeInstance["date_of_birth"] != '':  
        date_of_birth = datetime.now()
    
    query = update(Employee).values(name = employeeInstance["name"], 
                email = employeeInstance["email"], 
                date_of_birth = date_of_birth,
                description = employeeInstance["description"], 
                entity_id = int(employeeInstance["entity_id"]),
                user_id = int(employeeInstance["user_id"])).where(Employee.id == employee_id)

    return await database.execute(query)
