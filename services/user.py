from models.user import UserIn, User
from core.db import database
from sqlalchemy import select, insert
from sqlalchemy import exc
from pydantic import BaseModel, ValidationError, validator
import asyncpg

async def post_user(newUser : dict):
    query = insert(User).values(name = newUser.name, email = newUser.email, is_active = newUser.is_active,
                 is_company = newUser.is_company)
    try:
        record = await database.fetch_one(query)
    except asyncpg.exceptions.UniqueViolationError as e:
        raise ValueError('passwords do not match')
    
    query = select(User).where(User.id == record.id)
    instanceUser = await database.fetch_one(query)
    return dict(instanceUser)
    
    