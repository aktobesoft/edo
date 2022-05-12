from sqlalchemy import select, insert, update, delete
import asyncpg
from core.db import database
from common_module.urls_module import correct_datetime

from references.business_type.models import BusinessType, BusinessTypeIn

async def get_business_type_by_id(business_type_id: int):
    query = select(BusinessType).where(BusinessType.name == business_type_id)
    result = await database.fetch_one(query)
    return result

async def delete_business_type_by_id(business_type_id: int):
    query = delete(BusinessType).where(BusinessType.name == business_type_id)
    result = await database.execute(query)
    return result

async def get_business_type_list(limit: int = 100,skip: int = 0,**kwargs):

    # if(kwargs['nested']):
    #     return await get_counterparty_nested_list(limit, skip, **kwargs)
    if('optional' in kwargs and kwargs['optional']):
        return await get_business_type_options_list(limit, skip, **kwargs)

    query = select(BusinessType.id, BusinessType.name, BusinessType.full_name).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def get_business_type_options_list(limit: int = 100,skip: int = 0,**kwargs):
    query = select(BusinessType.name.label('value'), BusinessType.full_name.label('text')).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = {'value': rec['value'], 'text': rec['text']}
        listValue.append(recordDict) 
    return listValue

async def post_business_type(businessTypeInstance : dict):
    
    query = insert(BusinessType).values(
                name = businessTypeInstance["name"], 
                full_name = businessTypeInstance["full_name"])
    newBusinessTypeId = await database.execute(query)
    
    return {**businessTypeInstance, 'id': newBusinessTypeId}

async def update_business_type(businessTypeInstance: dict):

    query = update(BusinessType).values(
                name = businessTypeInstance["name"], 
                full_name = businessTypeInstance["full_name"]).where(
                    BusinessType.name == int(businessTypeInstance['id']))

    result = await database.execute(query)
    return businessTypeInstance