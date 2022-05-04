from sqlalchemy import select, insert, update, delete
import asyncpg
from core.db import database
from common_module.urls_module import correct_datetime

from references.approval_process.models import ApprovalProcess, ApprovalProcessIn

async def get_approval_process_by_id(approval_process_id: int):
    query = select(ApprovalProcess).where(ApprovalProcess.id == approval_process_id)
    result = await database.fetch_one(query)
    return result

async def delete_approval_process_by_id(approval_process_id: int):
    query = delete(ApprovalProcess).where(ApprovalProcess.id == approval_process_id)
    result = await database.execute(query)
    return result

async def get_approval_process_list(limit: int = 100,skip: int = 0,**kwargs):

    query = select(ApprovalProcess).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def post_approval_process(apInstance : dict):
    
    query = insert(ApprovalProcess).values(
                is_active = apInstance["is_active"], 
                document_id = int(apInstance["document_id"]),
                document_type_id = int(apInstance["document_type_id"]),
                entity_iin = apInstance["entity_iin"],
                approval_template_id = int(apInstance["approval_template_id"]),
                status = apInstance["status"])
    result = await database.execute(query)
    return {**apInstance, 'id': result}

async def update_approval_process(apInstance: dict):

    query = update(ApprovalProcess).values(
                is_active = apInstance["is_active"], 
                document_id = int(apInstance["document_id"]),
                document_type_id = int(apInstance["document_type_id"]),
                entity_iin = apInstance["entity_iin"],
                approval_template_id = int(apInstance["approval_template_id"]),
                status = apInstance["status"]).\
                    where(ApprovalProcess.id == int(apInstance['id']))

    result = await database.execute(query)
    return apInstance