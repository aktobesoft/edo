from sqlalchemy import select, insert, update, delete
import asyncpg
from core.db import database
from common_module.urls_module import correct_datetime

from references.approval_template_step.models import ApprovalTemplateStep, ApprovalTemplateStepIn

async def get_approval_template_step_by_id(approval_template_step_id: int):
    query = select(ApprovalTemplateStep).where(ApprovalTemplateStep.id == approval_template_step_id)
    result = await database.fetch_one(query)
    return result

async def delete_approval_template_step_by_id(approval_template_step_id: int):
    query = delete(ApprovalTemplateStep).where(ApprovalTemplateStep.id == approval_template_step_id)
    result = await database.execute(query)
    return result

async def get_approval_template_step_list(limit: int = 100,skip: int = 0,**kwargs):

    query = select(ApprovalTemplateStep).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def post_approval_template_step(atStepeInstance : dict):
    
    query = insert(ApprovalTemplateStep).values(
                level = int(atStepeInstance["level"]), 
                type = atStepeInstance["type"],
                entity_iin = atStepeInstance["entity_iin"],
                employee_id = int(atStepeInstance["employee_id"]),
                approval_template_id = int(atStepeInstance["approval_template_id"]))
    result = await database.execute(query)
    
    return {**atStepeInstance, 'id': result}

async def update_approval_template_step(atStepeInstance: dict):

    query = update(ApprovalTemplateStep).values(
                level = int(atStepeInstance["level"]), 
                type = atStepeInstance["type"],
                entity_iin = atStepeInstance["entity_iin"],
                employee_id = int(atStepeInstance["employee_id"]),
                approval_template_id = int(atStepeInstance["approval_template_id"])).\
                    where(ApprovalTemplateStep.id == int(atStepeInstance['id']))

    result = await database.execute(query)
    return atStepeInstance