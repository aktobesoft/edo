from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from core.db import database
import asyncpg
from datetime import date, datetime
from common_module.urls_module import correct_datetime
from references.business_type.models import BusinessType

from references.user.models import User
from references.entity.models import Entity
from references.counterparty.models import Counterparty, CounterpartyIn, CounterpartyOut

async def get_counterparty_by_iin(counterparty_iin: str, **kwargs):
    if(kwargs['nested']):
        return await get_counterparty_nested_by_id(counterparty_iin, **kwargs)
    query = select(Counterparty).where(Counterparty.iin == counterparty_iin)
    result = await database.fetch_one(query)
    if result==None:
        raise HTTPException(status_code=404, detail="Item not found")
    return result

async def get_counterparty_nested_by_id(counterparty_iin: str, **kwargs):
    query = select(Counterparty,
                BusinessType.name.label("name"), 
                BusinessType.full_name.label("full_name")).\
                    join(
                BusinessType, Counterparty.type_id == BusinessType.id, isouter=True).\
                    where(Counterparty.iin == counterparty_iin)
    result = await database.fetch_one(query)
    result['business_type']
    return result

async def delete_counterparty_by_iin(counterparty_iin: str):
    query = delete(Counterparty).where(Counterparty.iin == counterparty_iin)
    result = await database.execute(query)
    return result

async def get_counterparty_list(limit: int = 100, skip: int = 0, **kwargs)->list[Counterparty]:
    
    if(kwargs['nested']):
        return await get_counterparty_nested_list(limit, skip, **kwargs)
    if(kwargs['optional']):
        return await get_counterparty_options_list(limit, skip, **kwargs)

    query = select(Counterparty.id, 
                Counterparty.iin, 
                Counterparty.name,
                Counterparty.address, 
                Counterparty.comment, 
                Counterparty.contact, 
                Counterparty.type_id, 
                BusinessType.name.label("business_type_name"), 
                BusinessType.full_name.label("business_type_full_name")).\
                    join(
                BusinessType, Counterparty.type_id == BusinessType.id, isouter=True).\
                    limit(limit).offset(skip)
   
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        #recordDict['type'] = {'id': recordDict['type_id'],'name': recordDict['name'],'full_name': recordDict['full_name'],}
        listValue.append(recordDict)
    return listValue

async def get_counterparty_nested_list(limit: int = 100, skip: int = 0, **kwargs):
    query = select(Counterparty.id, 
                Counterparty.iin, 
                Counterparty.name,
                Counterparty.address, 
                Counterparty.comment, 
                Counterparty.contact, 
                Counterparty.type_id, 
                BusinessType.name.label("business_type_name"), 
                BusinessType.full_name.label("business_type_full_name")).\
                    join(
                BusinessType, Counterparty.type_id == BusinessType.id, isouter=True).\
                   limit(limit).offset(skip)
   
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['type'] = {'id': recordDict['type_id'],'name': recordDict['business_type_name'],'full_name': recordDict['business_type_full_name'],}
        listValue.append(recordDict)
    return listValue

async def get_counterparty_options_list(limit: int = 100, 
                        skip: int = 0,
                        **kwargs)->list[Counterparty]:
    query = select(Counterparty.iin.label('value'),
                Counterparty.iin,
                Counterparty.id, 
                Counterparty.name,
                BusinessType.name.label("type_name")).\
                    join(
                BusinessType, Counterparty.type_id == BusinessType.id, isouter=True).\
                limit(limit).offset(skip)
   
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = {}
        recordDict['value'] = rec['value']
        recordDict['text'] = '{0} "{1}" ({2})'.format(rec['type_name'],rec['name'],rec['iin'])
        listValue.append(recordDict)
    return listValue

async def post_counterparty(counterpartyInstance : dict):
    query = insert(Counterparty).values(
                name = counterpartyInstance["name"],
                iin = counterpartyInstance["iin"], 
                address = counterpartyInstance["address"], 
                comment = counterpartyInstance["comment"],
                contact = counterpartyInstance["contact"], 
                type_id = int(counterpartyInstance["type_id"]))
    newCounterpartyId = await database.execute(query)
        
    return {**counterpartyInstance, 'id': newCounterpartyId}

async def update_counterparty(counterpartyInstance : dict):
    query = update(Counterparty).values(
                name = counterpartyInstance["name"], 
                address = counterpartyInstance["address"], 
                comment = counterpartyInstance['comment'],
                contact = counterpartyInstance["contact"],
                type_id = int(counterpartyInstance["type_id"])).where(Counterparty.iin == counterpartyInstance['iin'])
    result = await database.execute(query)
    return {**counterpartyInstance}