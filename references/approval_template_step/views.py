from json import dumps
import random
from sqlalchemy import String, bindparam, func, select, insert, tuple_, update, delete
import asyncpg
import binascii
from core.db import database
from common_module.urls_module import correct_datetime

from references.approval_template_step.models import ApprovalTemplateStep, _ApprovalTemplateStepIn
from references.counterparty.models import counterparty_fillDataFromDict
from references.document_type.models import document_type_fillDataFromDict
from references.employee.models import Employee, employee_fillDataFromDict
from references.entity.models import Entity, entity_fillDataFromDict

async def get_approval_template_step_by_id(approval_template_step_id: int):
    query = select(ApprovalTemplateStep).where(ApprovalTemplateStep.id == approval_template_step_id)
    result = await database.fetch_one(query)
    return result

async def get_approval_template_step_list(approval_template_id: int, **kwargs):
    if (kwargs['nested']):
        return await get_approval_template_step_nested_list(approval_template_id, **kwargs)    

    query = select(ApprovalTemplateStep).\
            where(ApprovalTemplateStep.approval_template_id == int(approval_template_id)) 
   
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue


async def get_approval_template_step_nested_list(approval_template_id: int, **kwargs):
    query = select(ApprovalTemplateStep, 
                    Entity.id.label('entity_id'), 
                    Entity.iin.label('entity_iin'),
                    Entity.name.label('entity_name'),
                    Employee.id.label('employee_id'),
                    Employee.email.label('employee_email'),
                    Employee.name.label('employee_name')).\
                join(Entity, ApprovalTemplateStep.entity_iin == Entity.iin, isouter=True).\
                join(Employee, ApprovalTemplateStep.employee_id == Employee.id, isouter=True).\
                where(ApprovalTemplateStep.approval_template_id == int(approval_template_id)).\
                order_by(ApprovalTemplateStep.id)
    result = await database.fetch_all(query)
    listValue = []
    for record in result:
        recordDict = dict(record)
        recordDict['entity'] = entity_fillDataFromDict(recordDict)
        recordDict['employee'] = employee_fillDataFromDict(recordDict)
        listValue.append(recordDict)
    return listValue

async def delete_approval_template_step_by_id(approval_template_step_id: int):
    query = delete(ApprovalTemplateStep).where(ApprovalTemplateStep.id == approval_template_step_id)
    result = await database.execute(query)
    return result


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

async def update_approval_template_steps_by_approval_template_id(at_steps : list, approval_template_id: int):
    
    # Надо подумать нужна ли хэш функция
    # чтобы избежать обновления всех данных
    # посути данных должно быть не так много
    # но все же

    for at_item in at_steps:
        at_item['approval_template_id'] = approval_template_id

    update_query = update(ApprovalTemplateStep).\
            values(level = int(bindparam('level')), 
                type = bindparam('type'), 
                entity_iin = bindparam('entity_iin'),
                employee_id = int(bindparam('employee_id')),
                approval_template_id = int(bindparam('approval_template_id'))).\
            where((ApprovalTemplateStep.id == int(bindparam('id'))))
    result = await database.execute_many(str(update_query), at_steps)


async def post_approval_template_steps_by_approval_template_id(at_steps : list, approval_template_id: int):
    
    for at_item in at_steps:
        at_item['approval_template_id'] = approval_template_id

    query = insert(ApprovalTemplateStep).\
            values(level = int(bindparam('level')), 
            type = bindparam('type'), 
            entity_iin = bindparam('entity_iin'),
            employee_id = int(bindparam('employee_id')),
            approval_template_id = int(bindparam('approval_template_id')))
    result = await database.execute_many(str(query), at_steps) 

async def delete_approval_template_steps_by_approval_template_id(listID : list, approval_template_id: int):

    # listID = [dict(item)['id'] for item in at_steps]
    query = delete(ApprovalTemplateStep).\
            where((ApprovalTemplateStep.approval_template_id == approval_template_id) & (ApprovalTemplateStep.id.in_(listID)))
    result = await database.execute(query)

async def delete_all_approval_template_steps_by_approval_template_id(approval_template_id: int):

    query = delete(ApprovalTemplateStep).\
            where( ApprovalTemplateStep.approval_template_id == approval_template_id)
    result = await database.execute(query) 