from typing import List
from fastapi import APIRouter
from models.references import Entity, Notes, User, BusinessType
from schemas.references import EntityIn, EntityOut, BusinessTypeOut, UserOptionsOut, UserOut, NotesOut, BusinessTypeOptionsOut
from core.db import database
from sqlalchemy import select, insert, tuple_, join


apiRouter = APIRouter()

@apiRouter.get('/business_type/', response_model = List[BusinessTypeOut])
async def get_business_type_list(skip: int = 0, limit: int = 10):
    query = select(BusinessType.id, BusinessType.name, BusinessType.full_name)
    records = await database.fetch_all(query)
    listValue = []
    
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

@apiRouter.get('/business_type_options/', response_model = List[BusinessTypeOptionsOut])
async def get_business_type_options_list(skip: int = 0, limit: int = 10):
    query = select(BusinessType.id, BusinessType.name, BusinessType.full_name)
    records = await database.fetch_all(query)
    listValue = []
    
    for rec in records:
        recordDict = dict(rec)
        recordDictOption = {}
        recordDictOption['text'] =  recordDict['full_name']
        recordDictOption['value'] =  recordDict['id'] 
        listValue.append(recordDictOption) 
    return listValue

@apiRouter.get('/user_options/', response_model = List[UserOptionsOut])
async def get_user_options_list():
    query = select(User.id, User.email, User.is_active).where(User.is_active)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        print(rec)
        print(rec.id)
        recordDict = dict(rec)
        recordDictOption = {}
        recordDictOption['text'] =  recordDict['email']
        recordDictOption['value'] =  recordDict['id'] 
        listValue.append(recordDictOption) 
    return listValue

@apiRouter.get('/user/', response_model = List[UserOut])
async def get_user_list():
    query = select(User.id, User.email, User.is_active).where(User.is_active)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

# ---------------- entity ------------------
@apiRouter.get('/entity/', response_model = List[EntityOut])
async def get_entity_list():
    query = select(Entity.name, Entity.iin, Entity.address, Entity.comment, Entity.director, 
            Entity.director_phone, Entity.administrator, Entity.administrator_phone, Entity.token, Entity.startDate, 
            Entity.type_id, Entity.endDate, Entity.user_id)
    #query = select(Entity).join(User, Entity.user_id == User.id)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        #print(recordDict)
        # recordDict['user'] = {'id': recordDict['user_id'], 'email': recordDict['email'], 'is_active': recordDict['is_active']}
        listValue.append(recordDict)
    #print(records)
    return listValue

@apiRouter.post('/entity/', response_model = EntityOut)
async def post_entity(newEntity : EntityIn):
    query = insert(Entity).values(name = newEntity.name, address = newEntity.address, comment = newEntity.comment,
                 director = newEntity.director, director_phone = newEntity.director_phone, iin = newEntity.iin, 
                 administrator = newEntity.administrator, administrator_phone = newEntity.administrator_phone, 
                 startDate = newEntity.startDate, endDate = newEntity.endDate, type_id = newEntity.type_id, 
                 user_id = newEntity.user_id)
    record = await database.fetch_all(query)
    if len(record) == 1:
        query = select(Entity).where(Entity.id == record[0]['id'])
        records = await database.fetch_all(query)
        for rec in records:
            return dict(rec)
    #print(record)
    return record
     
# ---------------- notes ------------------
@apiRouter.get("/notes", response_model=List[NotesOut])
async def read_notes():
    # for i in range(100):
    #     query = insert(Notes).values(text ='{0} - {1}'.format("some text", i), completed = True)
    #     print(query)
    #     await database.fetch_all(query)
    list1 = [tuple_(50, True),tuple_(51, True)]
    query = select(Notes.id, Notes.text, Notes.completed).where(tuple_(Notes.id, Notes.completed).in_(list1))
    #print(query)
    listValue = await database.fetch_all(query)
    #print(listValue)
    return listValue