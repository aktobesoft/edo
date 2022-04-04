from typing import List

from databases import Database
from models.entity import Entity, EntityIn, EntityOut
from sqlalchemy import select
from core.db import database

async def get_entity_list(limit: int = 100, skip: int = 0, **kwargs)->list[Entity]:
    query = select(Entity.id, Entity.name, Entity.iin, Entity.address, Entity.comment, Entity.director, 
            Entity.director_phone, Entity.administrator, Entity.administrator_phone, Entity.token, Entity.startDate, 
            Entity.type_id, Entity.endDate, Entity.user_id).order_by(Entity.id).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        print(rec)
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue