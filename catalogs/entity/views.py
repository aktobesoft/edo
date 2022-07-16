from fastapi import HTTPException
from sqlalchemy import func, select, insert, update, delete
from catalogs.enum_types.views import business_type_fillDataFromDict
from core.db import database
import asyncpg
from common_module.urls_module import correct_datetime, is_need_filter

from catalogs.entity.models import Entity
from catalogs.enum_types.models import BusinessType


async def get_entity_by_id(entity_id: int, **kwargs):
    query = select(Entity).where(Entity.id == entity_id)
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(Entity.iin.in_(kwargs['entity_iin_list']))
    resultEntity = await database.fetch_one(query)
    return resultEntity

async def get_entity_by_iin(entity_iin: str, **kwargs):
    # RLS
    if(is_need_filter('entity_iin_list', kwargs) and entity_iin not in kwargs['entity_iin_list']):
        raise HTTPException(status_code=404, detail="Item not found")

    if kwargs['nested']:
        query = select(Entity.id, 
                Entity.name, 
                Entity.full_name,
                Entity.iin, 
                Entity.address, 
                Entity.comment, 
                Entity.director, 
                Entity.director_phone, 
                Entity.administrator, 
                Entity.administrator_phone, 
                Entity.token, 
                Entity.start_date, 
                Entity.type_name, 
                Entity.end_date, 
                BusinessType.id.label("business_type_id"), 
                BusinessType.name.label("business_type_name"),
                BusinessType.full_name.label("business_type_full_name")).\
                    join(BusinessType, Entity.type_name == BusinessType.name, isouter=True).\
                    where(Entity.iin == entity_iin)

    query = select(Entity).where(Entity.iin == entity_iin)
    result = await database.fetch_one(query)
    if result==None:
        raise HTTPException(status_code=404, detail="Item not found")
    return result

async def delete_entity_by_iin(entity_iin: str, **kwargs):
    # RLS
    if(is_need_filter('entity_iin_list', kwargs) and entity_iin not in kwargs['entity_iin_list']):
        raise HTTPException(status_code=404, detail="Item not found")

    query = delete(Entity).where(Entity.iin == entity_iin)
    resultEntity = await database.execute(query)
    return resultEntity

async def get_entity_count(**kwargs)->list[Entity]:
    query = select(func.count(Entity.id))
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(Entity.iin.in_(kwargs['entity_iin_list']))
    return await database.execute(query)

async def get_entity_list(limit: int = 100, skip: int = 0, **kwargs)->list[Entity]:
    
    if(kwargs['nested']):
        return await get_entity_nested_list(limit, skip, **kwargs)
    if('optional' in kwargs and kwargs['optional']):
        return await get_entity_options_list(limit, skip, **kwargs)

    query = select(Entity.id, 
                Entity.name, 
                Entity.full_name,
                Entity.iin, 
                Entity.address, 
                Entity.comment, 
                Entity.director, 
                Entity.director_phone, 
                Entity.administrator, 
                Entity.administrator_phone, 
                Entity.token, 
                Entity.start_date, 
                Entity.type_name, 
                Entity.end_date).limit(limit).offset(skip).order_by(Entity.name)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(Entity.iin.in_(kwargs['entity_iin_list']))  
          
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def get_entity_nested_list(limit: int = 100, skip: int = 0, **kwargs):
   
    query = select(Entity.id, 
                Entity.name, 
                Entity.full_name,
                Entity.iin, 
                Entity.address, 
                Entity.comment, 
                Entity.director, 
                Entity.director_phone, 
                Entity.administrator, 
                Entity.administrator_phone, 
                Entity.token, 
                Entity.start_date, 
                Entity.type_name, 
                Entity.end_date, 
                BusinessType.id.label("business_type_id"), 
                BusinessType.name.label("business_type_name"),
                BusinessType.full_name.label("business_type_full_name")).\
                    join(BusinessType, Entity.type_name == BusinessType.name, isouter=True).\
                    limit(limit).offset(skip)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(Entity.iin.in_(kwargs['entity_iin_list'])) 

    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['type'] = business_type_fillDataFromDict(rec)
        listValue.append(recordDict)
    return listValue

async def post_entity(entityInstance : dict, **kwargs):
    # RLS
    if(is_need_filter('entity_iin_list', kwargs) and entityInstance["iin"] not in kwargs['entity_iin_list']):
        raise HTTPException(status_code=403, detail="Forbidden")
    
    entityInstance["start_date"] = correct_datetime(entityInstance["start_date"])
    entityInstance["end_date"] = correct_datetime(entityInstance["end_date"])

    query = insert(Entity).values(
                name = entityInstance["name"], 
                full_name = entityInstance["full_name"],
                address = entityInstance["address"], 
                comment = entityInstance["comment"],
                director = entityInstance["director"], 
                director_phone = entityInstance["director_phone"], 
                iin = entityInstance["iin"], 
                administrator = entityInstance["administrator"], 
                administrator_phone = entityInstance["administrator_phone"], 
                start_date = entityInstance["start_date"], 
                end_date = entityInstance["end_date"], 
                type_name = entityInstance["type_name"], 
                token = '')

    try:
        newEntityId = await database.execute(query)
    except asyncpg.exceptions.ForeignKeyViolationError as e:
        raise ValueError('Не уникальный ИИН')
    return {**entityInstance, 'id': newEntityId}



async def update_entity(entityInstance: dict, entity_iin: str, **kwargs):
    # RLS
    if(is_need_filter('entity_iin_list', kwargs) and entityInstance["iin"] not in kwargs['entity_iin_list']):
        raise HTTPException(status_code=403, detail="Forbidden")

    entityInstance["start_date"] = correct_datetime(entityInstance["start_date"])
    entityInstance["end_date"] = correct_datetime(entityInstance["end_date"])
    
    query = update(Entity).values(
                name = entityInstance["name"],
                full_name = entityInstance["full_name"], 
                address = entityInstance["address"], 
                comment = entityInstance["comment"],
                director = entityInstance["director"], 
                director_phone = entityInstance["director_phone"], 
                iin = entityInstance["iin"], 
                administrator = entityInstance["administrator"], 
                administrator_phone = entityInstance["administrator_phone"], 
                start_date = entityInstance["start_date"], 
                end_date = entityInstance["end_date"] , 
                type_name = entityInstance["type_name"]).where(
                    Entity.iin == entity_iin)

    result = await database.execute(query)
    return entityInstance

async def get_entity_options_list(limit: int = 100, skip: int = 0, **kwargs):
    query = select(Entity.iin.label('value'), Entity.name.label('text')).limit(limit).offset(skip)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(Entity.iin.in_(kwargs['entity_iin_list']))
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        listValue.append(dict(rec))
    return listValue
