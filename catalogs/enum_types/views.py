from fastapi import HTTPException
from sqlalchemy import select
from core.db import database

from catalogs.enum_types.models import EnumBusinessType, EnumDocumentType

async def get_enum_business_type_list(limit: int = 100,skip: int = 0,**kwargs):

    # if(kwargs['nested']):
    #     return await get_counterparty_nested_list(limit, skip, **kwargs)
    if('optional' in kwargs and kwargs['optional']):
        return await get_enum_business_type_options_list(limit, skip, **kwargs)

    query = select(EnumBusinessType.id, EnumBusinessType.name, EnumBusinessType.full_name).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def get_enum_business_type_options_list(limit: int = 100,skip: int = 0,**kwargs):
    query = select(EnumBusinessType.name.label('value'), EnumBusinessType.full_name.label('text')).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = {'value': rec['value'], 'text': rec['text']}
        listValue.append(recordDict) 
    return listValue

async def get_enum_document_type_list(limit: int = 100,skip: int = 0,**kwargs):

    query = select(EnumDocumentType.id, EnumDocumentType.name, EnumDocumentType.metadata_name, EnumDocumentType.description).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def get_enum_document_type_id_by_metadata_name(metadata_name: str):
    query = select(EnumDocumentType.id).where(EnumDocumentType.metadata_name == metadata_name)
    result = await database.fetch_one(query)
    if result == None:
        raise HTTPException(status_code=404, detail="Item not found") 
    return result['id']

def enum_document_type_fillDataFromDict(queryResult : dict):
    return {
        'id': queryResult['enum_document_type_id'],
        'name': queryResult['enum_document_type_name'],
        'description': queryResult['enum_document_type_description']
        }

def enum_business_type_fillDataFromDict(queryResult : dict):
    return {
        'id': queryResult['enum_business_type_id'],
        'name': queryResult['enum_business_type_name'],
        'full_name': queryResult['enum_business_type_full_name'] 
        } 