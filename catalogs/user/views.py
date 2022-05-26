from catalogs.user.models import UserIn, User
from core.db import database
from sqlalchemy import delete, select, insert, update
from sqlalchemy import exc
from pydantic import BaseModel, ValidationError, validator
import asyncpg

async def post_user(newUser : dict):
    query = insert(User).values(name = newUser['name'], email = newUser['email'], is_active = newUser['is_active'],
                 is_company = newUser['is_company'])
    return await database.execute(query)

async def get_user_by_id(user_id: int):
    queryUser = select(User).where(User.id == user_id)
    resultUser = await database.fetch_one(queryUser)
    return resultUser 
    
async def get_user_list(limit: int = 100, skip: int = 0, **kwargs):

    query = select(User.id, User.name, User.email, User.is_active, User.is_company
            ).where(User.is_active).order_by(User.id).limit(limit).offset(skip)
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
    query = update(User).values(
                name = newUser['name'], 
                email = newUser['email'], 
                is_active = newUser['is_active'],
                is_company = newUser['is_company']).\
                    where(User.id == user_id)
    return await database.execute(query)






    