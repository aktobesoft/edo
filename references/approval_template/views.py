from sqlalchemy import select, insert, update, delete
import asyncpg
from core.db import database
from common_module.urls_module import correct_datetime

from references.approval_template.models import ApprovalTemplate, ApprovalTemplateIn

async def get_approval_template_by_id(approval_template_id: int):
    query = select(ApprovalTemplate).where(ApprovalTemplate.id == approval_template_id)
    result = await database.fetch_one(query)
    return result

async def delete_approval_template_by_id(approval_template_id: int):
    query = delete(ApprovalTemplate).where(ApprovalTemplate.id == approval_template_id)
    result = await database.execute(query)
    return result

async def get_approval_template_list(limit: int = 100,skip: int = 0,**kwargs):

    query = select(ApprovalTemplate).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    print(listValue)
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