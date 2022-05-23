from sqlalchemy import func, select, insert, update, delete
import asyncpg
from core.db import database
from common_module.urls_module import correct_datetime

from catalogs.document_type.models import DocumentType, DocumentTypeIn

async def get_document_type_by_id(document_type_id: int):
    query = select(DocumentType).where(DocumentType.id == document_type_id)
    result = await database.fetch_one(query)
    return result

async def delete_document_type_by_id(document_type_id: int):
    query = delete(DocumentType).where(DocumentType.id == document_type_id)
    result = await database.execute(query)
    return result

async def get_document_type_count():
    query = select(func.count(DocumentType.id))
    return await database.execute(query)

async def get_document_type_list(limit: int = 100,skip: int = 0,**kwargs):

    # if(kwargs['nested']):
    #     return await get_counterparty_nested_list(limit, skip, **kwargs)
    if('optional' in kwargs and kwargs['optional']):
        return await get_document_type_options_list(limit, skip, **kwargs)

    query = select(DocumentType.id, DocumentType.name, DocumentType.description).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def get_document_type_options_list(limit: int = 100,skip: int = 0,**kwargs):
    query = select(DocumentType.name.label('value'), DocumentType.description.label('text')).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = {'value': rec['value'], 'text': rec['text']}
        listValue.append(recordDict) 
    return listValue

async def post_document_type(businessTypeInstance : dict):
    
    query = insert(DocumentType).values(
                name = businessTypeInstance["name"], 
                description = businessTypeInstance["description"])
    newDocumentTypeId = await database.execute(query)
    
    return {**businessTypeInstance, 'id': newDocumentTypeId}

async def update_document_type(businessTypeInstance: dict, document_type_id):

    query = update(DocumentType).values(
                name = businessTypeInstance["name"], 
                description = businessTypeInstance["description"]).where(
                DocumentType.id == int(document_type_id))

    result = await database.execute(query)
    return businessTypeInstance