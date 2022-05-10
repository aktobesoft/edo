import json
from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
import asyncpg
from core.db import database
from common_module.urls_module import correct_datetime

from references.approval_template.models import ApprovalTemplate, ApprovalTemplateIn
from references.approval_template_step.views import get_approval_template_step_list, get_approval_template_step_nested_list,\
                post_approval_template_steps_by_approval_template_id, update_approval_template_steps_by_approval_template_id
from references.counterparty.models import Counterparty
from references.document_type.models import DocumentType, document_type_fillDataFromDict
from references.entity.models import Entity, entity_fillDataFromDict


async def get_approval_template_by_id(approval_template_id: int, **kwargs):
    if(kwargs['nested']):
        return await get_approval_template_nested_by_id(approval_template_id, **kwargs)
    query = select(ApprovalTemplate).where(ApprovalTemplate.id == approval_template_id)
    result = await database.fetch_one(query)
    if result == None:
        raise HTTPException(status_code=404, detail="Item not found")     
    return {**result, 'steps': await get_approval_template_step_list(approval_template_id,  **kwargs)}

async def get_approval_template_nested_by_id(approval_template_id: int, **kwargs):
    if approval_template_id == 0:
        result = ApprovalTemplateIn().json()
        print(result)
        return result
    query = select(ApprovalTemplate,
                    Entity.id.label('entity_id'), 
                    Entity.name.label('entity_name'), 
                    DocumentType.id.label('document_type_id'),
                    DocumentType.name.label('document_type_name'),
                    DocumentType.description.label('document_type_description')).\
            where(ApprovalTemplate.id == approval_template_id).\
        join(Entity, ApprovalTemplate.entity_iin == Entity.iin, isouter=True).\
        join(DocumentType, ApprovalTemplate.document_type_id == DocumentType.id, isouter=True)
    result = await database.fetch_one(query)
    recordDict = dict(result)
    recordDict['entity'] = entity_fillDataFromDict(recordDict)
    recordDict['document_type'] = document_type_fillDataFromDict(recordDict)
    return {**recordDict, 'steps': await get_approval_template_step_nested_list(approval_template_id, **kwargs)}

async def delete_approval_template_by_id(approval_template_id: int):
    query = delete(ApprovalTemplate).where(ApprovalTemplate.id == approval_template_id)
    result = await database.execute(query)
    return result

async def get_approval_template_list(limit: int = 100,skip: int = 0,**kwargs):
    
    if(kwargs['nested']):
        return await get_approval_template_nested_list(limit, skip, **kwargs)

    query = select(ApprovalTemplate).limit(limit).offset(skip).order_by(ApprovalTemplate.id)
    print(kwargs)
    if(kwargs['entity_iin']!=''):
        query = query.where(ApprovalTemplate.entity_iin == kwargs['entity_iin'])  
    records = await database.fetch_all(query)

    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def get_approval_template_nested_list(limit: int = 100,skip: int = 0,**kwargs):

    query = select(ApprovalTemplate, 
                    Entity.id.label('entity_id'), 
                    Entity.name.label('entity_name'), 
                    DocumentType.id.label('document_type_id'),
                    DocumentType.name.label('document_type_name'),
                    DocumentType.description.label('document_type_description')).\
                join(Entity, ApprovalTemplate.entity_iin == Entity.iin, isouter=True).\
                join(DocumentType, ApprovalTemplate.document_type_id == DocumentType.id, isouter=True).\
                limit(limit).offset(skip).order_by(ApprovalTemplate.id)
    if(kwargs['entity_iin']):
        query = query.where(ApprovalTemplate.entity_iin == kwargs['entity_iin'])    

    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['entity'] = entity_fillDataFromDict(recordDict)
        recordDict['document_type'] = document_type_fillDataFromDict(recordDict)
        listValue.append(recordDict)
    return listValue

async def post_approval_template(atInstance : dict):
    
    query = insert(ApprovalTemplate).values(
                document_type_id = int(atInstance["document_type_id"]), 
                name = atInstance["name"],
                entity_iin = atInstance["entity_iin"])
    result = await database.execute(query)
    if (len(atInstance["steps"]) >= 1):
        resultsteps = await post_approval_template_steps_by_approval_template_id(atInstance["steps"], result)
    return {**atInstance, 'id': result}

async def update_approval_template(atInstance: dict, approval_template_id: int):
    query = update(ApprovalTemplate).values(
                document_type_id = int(atInstance["document_type_id"]), 
                name = atInstance["name"],
                entity_iin = atInstance["entity_iin"]).\
                where(ApprovalTemplate.id == int(approval_template_id))

    result = await database.execute(query)
    resultsteps = await update_approval_template_steps_by_approval_template_id(atInstance["steps"], approval_template_id)
    return atInstance