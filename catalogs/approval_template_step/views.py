from json import dumps
import random
from sqlalchemy import Enum, String, bindparam, func, select, insert, tuple_, update, delete
from sqlalchemy.sql.expression import bindparam
import asyncpg
import binascii

from core.db import database
from common_module.urls_module import correct_datetime

from catalogs.approval_template_step.models import ApprovalTemplateStep, _ApprovalTemplateStepPUT
from catalogs.employee.models import Employee, employee_fillDataFromDict
from catalogs.enum_types.models import StepType

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
                    Employee.id.label('employee_id'),
                    Employee.email.label('employee_email'),
                    Employee.name.label('employee_name')).\
                join(Employee, ApprovalTemplateStep.employee_id == Employee.id, isouter=True).\
                where(ApprovalTemplateStep.approval_template_id == int(approval_template_id)).\
                order_by(ApprovalTemplateStep.id)
    result = await database.fetch_all(query)
    listValue = []
    for record in result:
        recordDict = dict(record)
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
                hash = atStepeInstance["hash"],
                employee_id = int(atStepeInstance["employee_id"]),
                approval_template_id = int(atStepeInstance["approval_template_id"]))
    result = await database.execute(query)
    
    return {**atStepeInstance, 'id': result}

async def update_approval_template_step(atStepeInstance: dict):

    query = update(ApprovalTemplateStep).values(
                level = int(atStepeInstance["level"]), 
                type = atStepeInstance["type"],
                hash = atStepeInstance["hash"],
                employee_id = int(atStepeInstance["employee_id"]),
                approval_template_id = int(atStepeInstance["approval_template_id"])).\
                    where(ApprovalTemplateStep.id == int(atStepeInstance['id']))

    result = await database.execute(query)
    return atStepeInstance

async def update_approval_template_steps_by_approval_template_id(at_steps : list, approval_template_id: int):

    listID = []
    listHashID = []
    newList = []

    # Надо подумать нужна ли хэш функция
    # чтобы избежать обновления всех данных
    # посути данных должно быть не так много
    # но все же
    
    for at_item in at_steps:
        at_item_dict = dict(at_item)
        listID.append(at_item_dict['id'])
        at_item_dict['approval_template_id'] = approval_template_id
        newList.append(at_item_dict)
        # listHashID.append(tuple_(dict_item['id'], dict_item['hash']))
        
    select1 = select(ApprovalTemplateStep.id, ApprovalTemplateStep.hash, func.lower("delete", type_=String).label('operation')).where(
                (ApprovalTemplateStep.approval_template_id == approval_template_id) & (ApprovalTemplateStep.id.not_in(listID)))
    
    # select2 = select(ApprovalTemplateStep.id, ApprovalTemplateStep.hash, func.lower("no_update", type_=String)).where(
    #             (ApprovalTemplateStep.approval_template_id == approval_template_id) & 
    #             (tuple_(ApprovalTemplateStep.id, ApprovalTemplateStep.hash).in_(listHashID)))
    
    # query = select1.union_all(select2).alias('pr_list')
    result = await database.fetch_all(select1)
    idListNoUpdate = []
    idListDelete = []

    listUpdate = []
    listInsert = []
    for item in result:
        if item['operation'] == 'delete':
            idListDelete.append(item['id'])    
        elif item['operation'] == 'no_update':
            idListNoUpdate.append(item['id'])

    # rrIndex = random.randint(0, len(idListNoUpdate))
    # index = 0
    
    for _at_step in at_steps:
        at_step = dict(_at_step)
        if (at_step['id'] in idListNoUpdate):
            # if (index == rrIndex):
            #     # рандомная проверка хэш записи
            #     # защита если кто то пытается специально посылать много записей с неправильной функции
            #     # чтобы загрузить сервис
            #     # надо придумать что делать в такой ситуации
            #     copyRecord = dict(_at_step)
            #     copyRecord.pop('hash')
            #     text = dumps(copyRecord, ensure_ascii=False, separators=(',', ':'))
            #     resultHash = binascii.crc32(text.encode('utf8'))
            #     if str(resultHash) != str(at_step['hash']):
            #         print('Внимание хэши не равны {0} и {1}'.format(str(at_step['hash']), resultHash))
            # index = index + 1
            continue
        elif (at_step['id'] == 0):
            # в первую запись всегда хэш будет другой потому как id пустой
            # во второй проход хэш уже будет правильный
            at_step.pop('id')
            at_step['approval_template_id'] = approval_template_id
            listInsert.append(at_step)
        elif (at_step['id'] not in idListDelete and at_step['id'] not in idListNoUpdate):
            at_step['approval_template_id'] = approval_template_id
            listUpdate.append(at_step)

    if(len(listUpdate)>0):
        update_query = update(ApprovalTemplateStep).\
            values(level = bindparam('level'), 
                type = bindparam('type'), 
                hash = bindparam('hash'),
                employee_id = bindparam('employee_id'),
                approval_template_id = bindparam('approval_template_id')).\
            where(ApprovalTemplateStep.id == bindparam('id'))
        result = await database.execute_many(str(update_query), newList)
    
    if(len(listInsert)>0):
        result = await post_approval_template_steps_by_approval_template_id(listInsert, approval_template_id)

    if(len(idListDelete)>0):
        result = await delete_approval_template_steps_by_approval_template_id(idListDelete, approval_template_id)  

    return at_steps 
    

    


async def post_approval_template_steps_by_approval_template_id(at_steps : list, approval_template_id: int):
    
    newList = []
    for at_item in at_steps:
        at_item_dict = dict(at_item)
        at_item_dict['approval_template_id'] = approval_template_id
        newList.append(at_item_dict)

    query = insert(ApprovalTemplateStep).\
            values(level = bindparam('level'), 
            type = bindparam('type'), 
            hash = bindparam('hash'),
            employee_id = bindparam('employee_id'),
            approval_template_id = bindparam('approval_template_id'))
    result = await database.execute_many(query, newList) 

async def delete_approval_template_steps_by_approval_template_id(listID : list, approval_template_id: int):

    # listID = [dict(item)['id'] for item in at_steps]
    query = delete(ApprovalTemplateStep).\
            where((ApprovalTemplateStep.approval_template_id == approval_template_id) & (ApprovalTemplateStep.id.in_(listID)))
    result = await database.execute(query)

async def delete_all_approval_template_steps_by_approval_template_id(approval_template_id: int):

    query = delete(ApprovalTemplateStep).\
            where( ApprovalTemplateStep.approval_template_id == approval_template_id)
    result = await database.execute(query) 