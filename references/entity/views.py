from sqlalchemy import select, insert, update, delete
from core.db import database
import asyncpg
from datetime import date, datetime
from common_module.urls_module import correct_datetime

from references.entity.models import Entity, EntityIn
from references.business_type.models import BusinessType, business_type_fillDataFromDict
from references.user.models import User, user_fillDataFromDict


async def get_entity_by_id(entity_id: int):
    queryEntity = select(Entity).where(Entity.id == entity_id)
    resultEntity = await database.fetch_one(queryEntity)
    return resultEntity

async def delete_entity_by_id(entity_id: int):
    queryEntity = delete(Entity).where(Entity.id == entity_id)
    resultEntity = await database.execute(queryEntity)
    return resultEntity

async def get_entity_list(limit: int = 100, skip: int = 0, **kwargs)->list[Entity]:
    
    if(kwargs['nested']):
        return await get_entity_nested_list(limit, skip, **kwargs)
    if(kwargs['optional']):
        return await get_entity_options_list(limit, skip, **kwargs)

    query = select(Entity.id, 
                Entity.name, 
                Entity.iin, 
                Entity.address, 
                Entity.comment, 
                Entity.director, 
                Entity.director_phone, 
                Entity.administrator, 
                Entity.administrator_phone, 
                Entity.token, 
                Entity.start_date, 
                Entity.type_id, 
                Entity.end_date, 
                Entity.user_id).order_by(
                    Entity.id).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def get_entity_nested_list(limit: int = 100, skip: int = 0, **kwargs)->list[Entity]:
   
    query = select(Entity.id, 
                Entity.name, 
                Entity.iin, 
                Entity.address, 
                Entity.comment, 
                Entity.director, 
                Entity.director_phone, 
                Entity.administrator, 
                Entity.administrator_phone, 
                Entity.token, 
                Entity.start_date, 
                Entity.type_id, 
                Entity.end_date, 
                Entity.user_id,
                BusinessType.id.label("business_type_id"), 
                BusinessType.name.label("business_type_name"),
                BusinessType.full_name.label("business_type_full_name"),
                User.email.label("user_email"), 
                User.name.label("user_name"),
                User.is_active.label("user_is_active"),
                User.is_company.label("user_is_company")).\
                    join(BusinessType, Entity.type_id == BusinessType.id, isouter=True).\
                    join(User, Entity.user_id == User.id, isouter=True).\
                    order_by(Entity.id).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['user'] = user_fillDataFromDict(recordDict)
        recordDict['type'] = business_type_fillDataFromDict(recordDict)
        listValue.append(recordDict)
    return listValue

async def post_entity(entityInstance : dict):
    
    entityInstance["start_date"] = correct_datetime(entityInstance["start_date"])
    entityInstance["end_date"] = correct_datetime(entityInstance["end_date"])

    query = insert(Entity).values(
                name = entityInstance["name"], 
                address = entityInstance["address"], 
                comment = entityInstance["comment"],
                director = entityInstance["director"], 
                director_phone = entityInstance["director_phone"], 
                iin = entityInstance["iin"], 
                administrator = entityInstance["administrator"], 
                administrator_phone = entityInstance["administrator_phone"], 
                start_date = entityInstance["start_date"], 
                end_date = entityInstance["end_date"], 
                type_id = int(entityInstance["type_id"]), 
                user_id = int(entityInstance["user_id"]), 
                token = '')
    try:
        newEntityId = await database.fetch_one(query)
    except asyncpg.exceptions.ForeignKeyViolationError as e:
        raise ValueError('Не уникальный ИИН')

    return {**entityInstance, 'id': newEntityId}



async def update_entity(entityInstance: dict):

    entityInstance["start_date"] = correct_datetime(entityInstance["start_date"])
    entityInstance["end_date"] = correct_datetime(entityInstance["end_date"])
    
    query = update(Entity).values(
                name = entityInstance["name"], 
                address = entityInstance["address"], 
                comment = entityInstance["comment"],
                director = entityInstance["director"], 
                director_phone = entityInstance["director_phone"], 
                iin = entityInstance["iin"], 
                administrator = entityInstance["administrator"], 
                administrator_phone = entityInstance["administrator_phone"], 
                start_date = entityInstance["start_date"], 
                end_date = entityInstance["end_date"] , 
                type_id = int(entityInstance["type_id"]), 
                user_id = int(entityInstance["user_id"]),
                token = entityInstance["token"]).where(
                    Entity.id == int(entityInstance['id']))

    result = await database.execute(query)
    return entityInstance

async def get_entity_options_list(limit: int = 100, skip: int = 0, **kwargs):
    query = select(Entity.id.label('value'), Entity.name.label('text')).order_by(Entity.id).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        listValue.append(dict(rec))
    return listValue