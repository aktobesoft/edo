import email
from typing import List, Optional
from fastapi import APIRouter, Depends
from models.entity import Entity, EntityIn, EntityOut
from services import entity, user
from models.business_type import BusinessTypeOut, BusinessTypeOptionsOut, BusinessType
from models.user import UserIn, UserOptionsOut, UserOut, User
from models.notes import NotesOut, Notes
from core.db import database
from sqlalchemy import select, insert, tuple_, join

async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

apiRouter = APIRouter()

@apiRouter.get('/business_type/', response_model = List[BusinessTypeOut])
async def get_business_type_list(commons: dict = Depends(common_parameters)):
    query = select(BusinessType.id, BusinessType.name, BusinessType.full_name)
    records = await database.fetch_all(query)
    listValue = []
    
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

@apiRouter.get('/business_type_options/', response_model = List[BusinessTypeOptionsOut])
async def get_business_type_options_list(commons: dict = Depends(common_parameters)):
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
async def get_user_options_list(commons: dict = Depends(common_parameters)):
    query = select(User.id.label('value'), User.email.label('text')).where(User.is_active)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        listValue.append(dict(rec))
    return listValue

@apiRouter.get('/user/', response_model = List[UserOut])
async def get_user_list(commons: dict = Depends(common_parameters)):
    query = select(User.id, User.name, User.email, User.is_active, User.is_company).where(User.is_active)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

# ---------------- entity ------------------
@apiRouter.get('/entity/', response_model=list[EntityOut])
async def get_entity_list(commons: dict = Depends(common_parameters)):
    return await entity.get_entity_list(**commons)

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
    return record

# ---------------- user ------------------
@apiRouter.post('/user/', response_model = UserOut)
async def post_user(newUser : UserIn):
    newUser = await user.post_user(newUser)
    return dict(newUser)
     
# ---------------- notes ------------------
@apiRouter.get("/notes", response_model=List[NotesOut])
async def read_notes(commons: dict = Depends(common_parameters)):
    list1 = [tuple_(50, True),tuple_(51, True)]
    query = select(Notes.id, Notes.text, Notes.completed).where(tuple_(Notes.id, Notes.completed).in_(list1))
    listValue = await database.fetch_all(query)
    return listValue