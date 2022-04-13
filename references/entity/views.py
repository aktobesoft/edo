from references.entity.models import Entity, EntityIn
from references.business_type.models import BusinessType
from references.user.models import User
from sqlalchemy import select, insert, update, delete
from core.db import database
import asyncpg
from datetime import date, datetime


async def get_entity_by_id(entity_id: int):
    queryEntity = select(Entity).where(Entity.id == entity_id)
    resultEntity = await database.fetch_one(queryEntity)
    return resultEntity

async def delete_entity_by_id(entity_id: int):
    queryEntity = delete(Entity).where(Entity.id == entity_id)
    resultEntity = await database.execute(queryEntity)
    print(resultEntity)
    return resultEntity

async def get_entity_list(limit: int = 100, 
                        skip: int = 0, 
                        addUser: bool = False, 
                        addBusinessType: bool = False,
                        **kwargs)->list[Entity]:
    if (addUser and addBusinessType):
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
                BusinessType.full_name.label("type_full_name"), 
                User.email.label("user_email"), 
                User.name.label("user_name")).join(
                BusinessType, Entity.type_id == BusinessType.id).join(
                User, Entity.user_id == User.id).order_by(
                    Entity.id).limit(limit).offset(skip)
    else:
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

async def post_entity(entityInstance : EntityIn):
    newEntity = dict(entityInstance)

    if type(newEntity["start_date"]) is date:
        start_date = newEntity["start_date"]
    elif type(newEntity["start_date"]) is str and newEntity["start_date"] != 'None' or newEntity["start_date"] != '': 
        start_date = datetime.now()
    
    if type(newEntity["start_date"]) is date:
        end_date = newEntity["end_date"]
    elif type(newEntity["end_date"]) is str and newEntity["end_date"] != 'None' or newEntity["end_date"] != '':  
        end_date = datetime.now()

    query = insert(Entity).values(name = newEntity["name"], address = newEntity["address"], comment = newEntity["comment"],
                director = newEntity["director"], director_phone = newEntity["director_phone"], iin = newEntity["iin"], 
                administrator = newEntity["administrator"], administrator_phone = newEntity["administrator_phone"], 
                start_date = start_date, end_date = end_date, type_id = int(newEntity["type_id"]), 
                user_id = int(newEntity["user_id"]), token = '')
    print(query)
    try:
        newEntity = await database.fetch_one(query)
    except asyncpg.exceptions.ForeignKeyViolationError as e:
        raise ValueError('Не уникальный ИИН')
    
    if newEntity != None:
        query = select(Entity).where(Entity.id == newEntity.id)
        record = await database.fetch_one(query)
        if (record != None):
            return dict(record)
    return EntityIn

async def update_entity(entity_id: int, entityInstance: dict):

    queryEntity = select(Entity).where(Entity.id == entity_id)
    resultEntity = await database.fetch_one(queryEntity)
    
    if resultEntity==None:
        return resultEntity

    start_date = entityInstance["start_date"]
    end_date = entityInstance["end_date"]

    if type(entityInstance["start_date"]) is date:
        start_date = entityInstance["start_date"]
    elif type(entityInstance["start_date"]) is str and entityInstance["start_date"] != 'None' or entityInstance["start_date"] != '': 
        start_date = datetime.now()
    
    if type(entityInstance["start_date"]) is date:
        end_date = entityInstance["end_date"]
    elif type(entityInstance["end_date"]) is str and entityInstance["end_date"] != 'None' or entityInstance["end_date"] != '':  
        end_date = datetime.now()
    
    query = update(Entity).values(name = entityInstance["name"], address = entityInstance["address"], comment = entityInstance["comment"],
                director = entityInstance["director"], director_phone = entityInstance["director_phone"], iin = entityInstance["iin"], 
                administrator = entityInstance["administrator"], administrator_phone = entityInstance["administrator_phone"], 
                start_date = start_date, end_date = end_date, type_id = int(entityInstance["type_id"]), 
                user_id = int(entityInstance["user_id"])).where(Entity.id == entity_id)

    print(start_date)
    print(end_date)
    print(query)
    return await database.execute(query)

async def get_entity_options_list(limit: int = 100, skip: int = 0, **kwargs):
    query = select(Entity.id.label('value'), Entity.name.label('text')
            ).order_by(Entity.id).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        listValue.append(dict(rec))
    return listValue
