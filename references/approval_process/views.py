from tkinter.tix import Tree
from typing import List
from datetime import date, datetime
import databases
from sqlalchemy import false, func, select, insert, true, update, delete
import asyncpg
from core.db import database
from common_module.urls_module import correct_datetime, qp_select_list

from references.approval_process.models import ApprovalProcess, ApprovalProcessIn
from references.approval_template.models import ApprovalTemplate
from references.approval_template_step.models import ApprovalTemplateStep
from references.approval_template_step.views import get_approval_template_step_list, get_approval_template_step_nested_list
from references.approval_route.views import post_approval_route, post_many_approval_route, get_approval_route_by_aproval_process_id
from references.enum_types.models import status_type

async def get_approval_process_by_id(approval_process_id: int):
    query = select(ApprovalProcess).\
                where((ApprovalProcess.id == approval_process_id) & (ApprovalProcess.is_active))
    result = await database.fetch_one(query)
    return result

async def delete_approval_process_by_id(approval_process_id: int):
    query = delete(ApprovalProcess).where(ApprovalProcess.id == approval_process_id)
    result = await database.execute(query)
    return result

async def get_approval_process_list(limit: int = 100,skip: int = 0,**kwargs):

    query = select(ApprovalProcess).limit(limit).offset(skip).\
                where(ApprovalProcess.is_active)
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
                start_date = apInstance["start_date"],
                end_date = apInstance["end_date"],
                status = apInstance["status"])
    result = await database.execute(query)
    return {**apInstance, 'id': result}

async def update_approval_process(approval_process_id: int, apInstance: dict):

    query = update(ApprovalProcess).values(
                is_active = apInstance["is_active"], 
                document_id = int(apInstance["document_id"]),
                document_type_id = int(apInstance["document_type_id"]),
                entity_iin = apInstance["entity_iin"],
                approval_template_id = int(apInstance["approval_template_id"]),
                start_date = apInstance["start_date"],
                end_date = apInstance["end_date"],
                status = apInstance["status"]).\
                    where(ApprovalProcess.id == approval_process_id)

    result = await database.execute(query)
    return apInstance

async def start_approval_process(parametrs):
    
    responseMap = {
        'Error': False,
        'Text': '',
        'ApprovalProcess': None, 
        'ApprovalProcessStatus': None, 
        'ApprovalRoute': [], 
        'ApprovalTemplate': None, 
        'ApprovalRouteCurrentStep':[]
        }

    parametrs['is_active'] = True
    resultMap = await check_approval_processes(parametrs)
    process_started = parametrs['document_id'] in resultMap

    if process_started:
        approval_processes = resultMap[parametrs['document_id']]
        if(approval_processes['status'] == status_type.signed or approval_processes['status'] == status_type.in_process):
            responseMap['Error'] = True
            responseMap['Text'] = 'Документу {0} уже согласован и подписан'.format(parametrs['document_id']) if approval_processes['status'] == status_type.signed else \
                                    'По документу "{0}" найден актуальный запущенный процесс со статусом "{1}"'.format(parametrs['document_id'], status_type.in_process.value)
            responseMap['ApprovalProcess'] = {
                                        'is_active': approval_processes['is_active'],
                                        'document_id': approval_processes['document_id'],
                                        'document_type_id': approval_processes['document_type_id'],
                                        'entity_iin': approval_processes['entity_iin'],
                                        'approval_template_id': approval_processes['approval_template_id'],
                                        'status': approval_processes['status'],
                                        'start_date': approval_processes['start_date'],
                                        'end_date': approval_processes['end_date'],
                                        'id': approval_processes['id']   
                                    }
            responseMap['ApprovalProcessStatus'] = approval_processes['status']
            responseMap['ApprovalRoute'] =  await get_approval_route_by_aproval_process_id(approval_processes['id']) 

    if process_started and 'approval_template_id' in approval_processes:
        # Ищем шаблон по "approval_template_id" актуального процесса
        query = select(ApprovalTemplate.id, ApprovalTemplate.name).\
                where(ApprovalTemplate.id == approval_processes['approval_template_id'])
    else:
        # Ищем шаблон если нет актуального процесса
        query = select(ApprovalTemplate.id, ApprovalTemplate.name).\
                where((ApprovalTemplate.entity_iin == parametrs['entity_iin']) & (ApprovalTemplate.document_type_id == parametrs['document_type_id'])).limit(1)
    
    approval_template = await database.fetch_one(query)
    if approval_template == None:
        responseMap['Error'] = True
        responseMap['Text'] = 'Не найден шаблон согласования по документу'
        return responseMap

    responseMap['ApprovalTemplate'] = {'id': approval_template['id'], 'name': approval_template['name']}

    # Дальше ищем его шаги
    query = select(ApprovalTemplateStep.employee_id, ApprovalTemplateStep.level, ApprovalTemplateStep.type).\
            where(ApprovalTemplateStep.approval_template_id == approval_template['id']).order_by(ApprovalTemplateStep.level, ApprovalTemplateStep.type)
    _qp_select_list = {'nested': false}
    approval_template_steps = await get_approval_template_step_list(approval_template['id'], **_qp_select_list)
    if len(approval_template_steps) == 0:
        responseMap['Error'] = True
        responseMap['Text'] = 'Не настроены шаги согласования в шаблоне'
        return responseMap

    # Есть запущенный процесс согласования, так что уходит отсюда
    # а то что уходиv только сейчас, выше нужно было создать информацию по шаблону согласования и шагаъ его
    if process_started and responseMap['Error']:
        return responseMap
   
    # ------------------------------ СОЗДАНИЕ ПРОЦЕССА -------------------------------
    
    # если все норм то создаем сам процесс
    apInstance = {
        'is_active': True,
        'document_id': parametrs['document_id'],
        'document_type_id': parametrs['document_type_id'],
        'entity_iin': parametrs['entity_iin'],
        'approval_template_id': approval_template['id'],
        'status': status_type.in_process,
        'start_date': date.today(),
        'end_date': None
    }

    responseMap['ApprovalProcess'] = await post_approval_process(apInstance)
    responseMap['ApprovalProcessStatus'] = status_type.in_process
    responseMap['Text'] = 'Процесс согласования запущен'

    # Создаем шаги согласования
    listRout = []
    for item in approval_template_steps:
        rout_step = {
            'is_active': True,
            'level': item['level'],
            'type': item['type'],
            'document_id': parametrs['document_id'],
            'document_type_id': parametrs['document_type_id'],
            'entity_iin': parametrs['entity_iin'],
            'employee_id': item['employee_id'],
            'approval_template_id': approval_template['id'],
            'approval_process_id': responseMap['ApprovalProcess']['id'],
        }
        listRout.append(rout_step) 
    
    await post_many_approval_route(listRout)
    responseMap['ApprovalRoute'] =  await get_approval_route_by_aproval_process_id(responseMap['ApprovalProcess']['id'])
    return responseMap

async def check_approval_processes(parametrs):
    
    responseMap = {}

    # Делаем массив
    if type(parametrs['document_id']) is int:
        listId = [parametrs['document_id']]
    else: 
        listId = parametrs['document_id'] 

    query = select( 
            ApprovalProcess.is_active,
            ApprovalProcess.document_id,
            ApprovalProcess.document_type_id, 
            ApprovalProcess.entity_iin,
            ApprovalProcess.approval_template_id,
            ApprovalProcess.status,
            ApprovalProcess.start_date,
            ApprovalProcess.end_date, 
            func.max(ApprovalProcess.id).label('id')).\
                where(
                    (ApprovalProcess.entity_iin == parametrs['entity_iin']) & 
                    (ApprovalProcess.is_active == parametrs['is_active']) & 
                    (ApprovalProcess.document_id.in_(listId)) & 
                    (ApprovalProcess.document_type_id == parametrs['document_type_id'])).\
                group_by(ApprovalProcess.entity_iin, 
                        ApprovalProcess.document_type_id,
                        ApprovalProcess.approval_template_id, 
                        ApprovalProcess.status,
                        ApprovalProcess.is_active,
                        ApprovalProcess.document_id,
                        ApprovalProcess.start_date,
                        ApprovalProcess.end_date)

    result = await database.fetch_all(query)

    if len(result)>0:
        for item in result:
            responseMap[item['document_id']] = dict(item)

    
    return responseMap

async def cancel_approval_process(parametrs):
    
    apInstance = {
        'is_active': False,
        'document_id': parametrs['document_id'],
        'document_type_id': parametrs['document_type_id'],
        'entity_iin': parametrs['entity_iin']
        }

    query = update(ApprovalProcess).values(
                    is_active = False, 
                    status = status_type.canceled,
                    end_date = date.today()).\
                where(
                    (ApprovalProcess.document_id == parametrs['document_id']) &
                    (ApprovalProcess.document_type_id == parametrs['document_type_id']) &
                    (ApprovalProcess.entity_iin == parametrs['entity_iin']))

    result = await database.execute(query)
    return apInstance



