import json
from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
import asyncpg
from catalogs.enum_types.views import enum_document_type_fill_data_from_dict
from core.db import database
from common_module.urls_module import correct_datetime, is_need_filter

from catalogs.approval_template.models import ApprovalTemplate, ApprovalTemplateIn
from catalogs.approval_template_step.views import get_approval_template_step_list, get_approval_template_step_nested_list,\
                post_approval_template_steps_by_approval_template_id, update_approval_template_steps_by_approval_template_id
from catalogs.counterparty.models import Counterparty
from catalogs.enum_types.models import EnumDocumentType
from catalogs.entity.models import Entity, entity_fill_data_from_dict


async def get_approval_template_by_id(approval_template_id: int, **kwargs):
    if(kwargs['nested']):
        return await get_approval_template_nested_by_id(approval_template_id, **kwargs)
    query = select(ApprovalTemplate).where(ApprovalTemplate.id == approval_template_id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(ApprovalTemplate.entity_iin.in_(kwargs['entity_iin_list']))
    result = await database.fetch_one(query)
    if result == None:
        raise HTTPException(status_code=404, detail="Item not found")     
    return {**result, 'steps': await get_approval_template_step_list(approval_template_id,  **kwargs)}

async def get_approval_template_nested_by_id(approval_template_id: int, **kwargs):
    if approval_template_id == 0:
        result = ApprovalTemplateIn().json()
        return result
    query = select(ApprovalTemplate,
                    Entity.id.label('entity_id'), 
                    Entity.name.label('entity_name'), 
                    EnumDocumentType.id.label('enum_document_type_id'),
                    EnumDocumentType.name.label('enum_document_type_name'),
                    EnumDocumentType.description.label('enum_document_type_description')).\
            where(ApprovalTemplate.id == approval_template_id).\
        join(Entity, ApprovalTemplate.entity_iin == Entity.iin, isouter=True).\
        join(EnumDocumentType, ApprovalTemplate.enum_document_type_id == EnumDocumentType.id, isouter=True)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(ApprovalTemplate.entity_iin.in_(kwargs['entity_iin_list']))
    result = await database.fetch_one(query)
    if result == None:
        raise HTTPException(status_code=404, detail="Item not found")
    recordDict = dict(result)
    recordDict['entity'] = entity_fill_data_from_dict(recordDict)
    recordDict['enum_document_type'] = enum_document_type_fill_data_from_dict(recordDict)
    return {**recordDict, 'steps': await get_approval_template_step_nested_list(approval_template_id, **kwargs)}

async def delete_approval_template_by_id(approval_template_id: int, **kwargs):
    query = delete(ApprovalTemplate).where(ApprovalTemplate.id == approval_template_id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(ApprovalTemplate.entity_iin.in_(kwargs['entity_iin_list']))
    result = await database.execute(query)
    return result

async def get_approval_template_list(limit: int = 100,skip: int = 0,**kwargs):
    
    if(kwargs['nested']):
        return await get_approval_template_nested_list(limit, skip, **kwargs)

    query = select(ApprovalTemplate).limit(limit).offset(skip).order_by(ApprovalTemplate.id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(ApprovalTemplate.entity_iin.in_(kwargs['entity_iin_list']))  
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
                    EnumDocumentType.id.label('enum_document_type_id'),
                    EnumDocumentType.name.label('enum_document_type_name'),
                    EnumDocumentType.description.label('enum_document_type_description')).\
                join(Entity, ApprovalTemplate.entity_iin == Entity.iin, isouter=True).\
                join(EnumDocumentType, ApprovalTemplate.enum_document_type_id == EnumDocumentType.id, isouter=True).\
                limit(limit).offset(skip).order_by(ApprovalTemplate.id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(ApprovalTemplate.entity_iin.in_(kwargs['entity_iin_list']))    

    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['entity'] = entity_fill_data_from_dict(recordDict)
        recordDict['enum_document_type'] = enum_document_type_fill_data_from_dict(recordDict)
        listValue.append(recordDict)
    return listValue

async def post_approval_template(atInstance : dict, **kwargs):
    # RLS
    if(is_need_filter('entity_iin_list', kwargs) and atInstance["entity_iin"] not in kwargs['entity_iin_list']):
        raise HTTPException(status_code=403, detail="Forbidden")

    query = insert(ApprovalTemplate).values(
                enum_document_type_id = int(atInstance["enum_document_type_id"]), 
                name = atInstance["name"],
                entity_iin = atInstance["entity_iin"])
    result = await database.execute(query)
    if (len(atInstance["steps"]) >= 1):
        resultsteps = await post_approval_template_steps_by_approval_template_id(atInstance["steps"], result)
    return {**atInstance, 'id': result}

async def update_approval_template(atInstance: dict, approval_template_id: int, **kwargs):
    query = update(ApprovalTemplate).values(
                enum_document_type_id = int(atInstance["enum_document_type_id"]), 
                name = atInstance["name"],
                entity_iin = atInstance["entity_iin"]).\
                where(ApprovalTemplate.id == int(approval_template_id))
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(ApprovalTemplate.entity_iin.in_(kwargs['entity_iin_list']))
    result = await database.execute(query)
    resultsteps = await update_approval_template_steps_by_approval_template_id(atInstance["steps"], approval_template_id)
    return atInstance