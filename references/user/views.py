from references.user.models import UserIn, User
from core.db import database
from sqlalchemy import select, insert
from sqlalchemy import exc
from pydantic import BaseModel, ValidationError, validator
import asyncpg

async def post_user(newUser : dict):
    query = insert(User).values(name = newUser.name, email = newUser.email, is_active = newUser.is_active,
                 is_company = newUser.is_company)
    try:
        record = await database.execute(query)
    except asyncpg.exceptions.UniqueViolationError as e:
        raise ValueError('passwords do not match')
    
    query = select(User).where(User.id == record.id)
    instanceUser = await database.fetch_one(query)
    return dict(instanceUser)
    
async def get_user_list(limit: int = 100, skip: int = 0, **kwargs):

    if(kwargs['optional']):
        return await get_user_options_list(limit, skip, **kwargs)

    query = select(User.id, User.name, User.email, User.is_active, User.is_company
            ).where(User.is_active).order_by(User.id).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def get_user_options_list(limit: int = 100, skip: int = 0, **kwargs):
    query = select(User.id.label('value'), User.email.label('text')
            ).where(User.is_active).order_by(User.id).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        listValue.append(dict(rec))
    return listValue

    