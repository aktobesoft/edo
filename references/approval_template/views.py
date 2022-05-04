from sqlalchemy import select, insert, update, delete
import asyncpg
from core.db import database
from common_module.urls_module import correct_datetime

from references.approval_template.models import ApprovalTemplate, ApprovalTemplateIn
from references.approval_template_step.views import get_approval_template_step_list
from references.counterparty.models import Counterparty
from references.document_type.models import DocumentType, document_type_fillDataFromDict
from references.entity.models import Entity, entity_fillDataFromDict

async def get_approval_template_by_id(approval_template_id: int):
    query = select(ApprovalTemplate).where(ApprovalTemplate.id == approval_template_id)
    result = await database.fetch_one(query)
    params = {}
    params['approval_template_id'] = approval_template_id
    return {**result, 'items': await get_approval_template_step_list(**params)}

async def delete_approval_template_by_id(approval_template_id: int):
    query = delete(ApprovalTemplate).where(ApprovalTemplate.id == approval_template_id)
    result = await database.execute(query)
    return result

async def get_approval_template_list(limit: int = 100,skip: int = 0,**kwargs):
    
    if(kwargs['nested']):
        return await get_approval_template_nested_list(limit, skip, **kwargs)

    query = select(ApprovalTemplate).limit(limit).offset(skip)
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
                limit(limit).offset(skip)
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
    return {**atInstance, 'id': result}

async def update_approval_template(atInstance: dict):

    query = update(ApprovalTemplate).values(
                document_type_id = int(atInstance["document_type_id"]), 
                name = atInstance["name"],
                entity_iin = atInstance["entity_iin"]).\
                    where(ApprovalTemplate.id == int(atInstance['id']))

    result = await database.execute(query)
    return atInstance