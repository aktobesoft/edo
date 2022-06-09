from datetime import date
from fastapi import HTTPException
from sqlalchemy import false, func, select, insert, update, delete
from core.db import database
from documents.purchase_requisition.models import PurchaseRequisition

from catalogs.approval_process.models import ApprovalProcess
from catalogs.approval_template.models import ApprovalTemplate, approval_template_fillDataFromDict
from catalogs.approval_template_step.models import ApprovalTemplateStep
from catalogs.approval_template_step.views import get_approval_template_step_list
from catalogs.approval_route.views import delete_approval_routes_by_approval_process_id, get_approval_route_by_aproval_process_id,\
                 post_approval_routes_by_approval_process_id, get_approval_route_nested_by_aproval_process_id, update_approval_routes_by_approval_process_id
from catalogs.document_type.models import DocumentType, document_type_fillDataFromDict
from catalogs.entity.models import Entity, entity_fillDataFromDict

async def collectRoutes(list_of_object: list, approval_process_id):
    listDict = []
    for item in list_of_object:
        itemDict = dict(item)
        # itemDict['type'] = 'line' if itemDict['type'] == StepType.line else 'paralel'
        itemDict['approval_process_id'] = approval_process_id
        listDict.append(itemDict)
    return listDict

async def get_approval_process_by_id(approval_process_id: int, **kwargs):
    kwargs['id'] = approval_process_id 
    if(kwargs['nested']): 
        result = await get_approval_process_nested_list(1,0, **kwargs)
        routes = await get_approval_route_nested_by_aproval_process_id(approval_process_id)
    else:
        result = await get_approval_process_list(1,0, **kwargs)
        routes = await get_approval_route_by_aproval_process_id(approval_process_id)
    
    if len(result)>0:
        return {**result[0], 'routes': routes}
    else:
        raise HTTPException(status_code=404, detail="Item not found") 

async def delete_approval_process_by_id(approval_process_id: int):
    resultDelete = await delete_approval_routes_by_approval_process_id(approval_process_id)
    query = delete(ApprovalProcess).where(ApprovalProcess.id == approval_process_id)
    result = await database.execute(query)
    return result

async def get_approval_process_list(limit: int = 100,skip: int = 0,**kwargs):

    if(kwargs['nested']):
        return await get_approval_process_nested_list(limit, skip, **kwargs)

    query = select(ApprovalProcess).limit(limit).offset(skip).\
                where((ApprovalProcess.is_active))#&(ApprovalProcess.entity_iin.in_(kwargs['entity_iin'])))
    if('id' in kwargs and kwargs['id']):
        query = query.where(ApprovalProcess.id == int(kwargs['id']))
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def get_approval_process_nested_list(limit: int = 100,skip: int = 0,**kwargs):
    # Будем делать Union all, потому как левое соединение со всеми таблицами рождает нагрузку на субд
    query_AR = select(ApprovalProcess,
                    PurchaseRequisition.number.label('number'),
                    PurchaseRequisition.date.label('date'),
                    DocumentType.description.label('document_type_description'),
                    DocumentType.name.label('document_type_name'),
                    ApprovalTemplate.name.label('approval_template_name'),
                    ApprovalTemplate.id.label('approval_template_id'),
                    Entity.name.label("entity_name"),
                    Entity.iin.label("entity_iin"),
                    Entity.id.label("entity_id")).\
                join(ApprovalProcess, ((PurchaseRequisition.id == ApprovalProcess.document_id) & (PurchaseRequisition.document_type_id == ApprovalProcess.document_type_id))).\
                join(ApprovalTemplate, (ApprovalTemplate.id == ApprovalProcess.approval_template_id)).\
                join(Entity, (Entity.iin == ApprovalProcess.entity_iin)).\
                join(DocumentType, (DocumentType.id == ApprovalProcess.document_type_id)).\
                where(ApprovalProcess.is_active).\
                limit(limit).offset(skip)
    if('id' in kwargs and kwargs['id']):
        query_AR = query_AR.where(ApprovalProcess.id == int(kwargs['id']))
    # query = query_purchase_requisition.union_all(select2).alias('pr_list')
    query = query_AR
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['document_type'] = document_type_fillDataFromDict(recordDict)
        recordDict['document'] = {'number': recordDict['number'], 'date': recordDict['date']}
        recordDict['entity'] = entity_fillDataFromDict(recordDict)
        recordDict['approval_template'] = approval_template_fillDataFromDict(recordDict)
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
    routesResult = await post_approval_routes_by_approval_process_id(await collectRoutes(apInstance['routes'], result))
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
    routesResult = await update_approval_routes_by_approval_process_id(await collectRoutes(apInstance['routes'], approval_process_id), approval_process_id)
    return apInstance

async def start_approval_process(parameters):
    
    responseMap = {
        'Error': False,
        'Text': '',
        'ApprovalProcess': None, 
        'ApprovalProcessStatus': None, 
        'ApprovalRoute': [], 
        'ApprovalTemplate': None, 
        'ApprovalRouteCurrentStep':[]
        }

    parameters['is_active'] = True
    resultMap = await check_approval_processes(parameters)
    process_started = parameters['document_id'] in resultMap

    if process_started:
        approval_processes = resultMap[parameters['document_id']]
        if(str(approval_processes['status']).lower() == "подписан" or str(approval_processes['status']).lower() == "в работе"):
            responseMap['Error'] = True
            responseMap['Text'] = 'Документу {0} уже согласован и подписан'.format(parameters['document_id']) if str(approval_processes['status']).lower() == "подписан" else \
                                    'По документу "{0}" найден актуальный запущенный процесс со статусом "{1}"'.format(parameters['document_id'], approval_processes['status'])
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
                where((ApprovalTemplate.entity_iin == parameters['entity_iin']) & (ApprovalTemplate.document_type_id == parameters['document_type_id'])).limit(1)
    
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
    
    

    # Создаем шаги согласования
    listRoutes = []
    for item in approval_template_steps:
        rout_step = {
            'is_active': True,
            'level': item['level'],
            'type': item['type'],
            'document_id': parameters['document_id'],
            'document_type_id': parameters['document_type_id'],
            'entity_iin': parameters['entity_iin'],
            'employee_id': item['employee_id'],
            'approval_template_id': approval_template['id'],
            'approval_process_id': 0,
            'hash': '',
        }
        listRoutes.append(rout_step) 

    # если все норм то создаем сам процесс
    apInstance = {
        'is_active': True,
        'document_id': parameters['document_id'],
        'document_type_id': parameters['document_type_id'],
        'entity_iin': parameters['entity_iin'],
        'approval_template_id': approval_template['id'],
        'status': 'в работе',
        'start_date': date.today(),
        'end_date': None,
        'routes': listRoutes
    }

    responseMap['ApprovalProcess'] = await post_approval_process(apInstance)
    responseMap['ApprovalProcessStatus'] = "в работе"
    responseMap['Text'] = 'Процесс согласования запущен'
    responseMap['ApprovalRoute'] =  await get_approval_route_by_aproval_process_id(responseMap['ApprovalProcess']['id'])

    # # Создаем шаги согласования
    # listRout = []
    # for item in approval_template_steps:
    #     rout_step = {
    #         'is_active': True,
    #         'level': item['level'],
    #         'type': item['type'],
    #         'document_id': parameters['document_id'],
    #         'document_type_id': parameters['document_type_id'],
    #         'entity_iin': parameters['entity_iin'],
    #         'employee_id': item['employee_id'],
    #         'approval_template_id': approval_template['id'],
    #         'approval_process_id': responseMap['ApprovalProcess']['id'],
    #         'hash': '',
    #     }
    #     listRout.append(rout_step) 
    # print(listRout)
    # await post_approval_routes_by_approval_process_id(listRout)
    # responseMap['ApprovalRoute'] =  await get_approval_route_by_aproval_process_id(responseMap['ApprovalProcess']['id'])
    return responseMap

async def check_approval_processes(parameters):
    
    responseMap = {}

    # Делаем массив
    if type(parameters['document_id']) is int:
        listId = [parameters['document_id']]
    else: 
        listId = parameters['document_id'] 

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
                    (ApprovalProcess.entity_iin == parameters['entity_iin']) & 
                    (ApprovalProcess.is_active == parameters['is_active']) & 
                    (ApprovalProcess.document_id.in_(listId)) & 
                    (ApprovalProcess.document_type_id == parameters['document_type_id'])).\
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

async def cancel_approval_process(parameters):
    
    apInstance = {
        'is_active': False,
        'document_id': parameters['document_id'],
        'document_type_id': parameters['document_type_id'],
        'entity_iin': parameters['entity_iin']
        }

    query = update(ApprovalProcess).values(
                    is_active = False, 
                    status = "отменен",
                    end_date = date.today()).\
                where(
                    (ApprovalProcess.document_id == int(parameters['document_id'])) &
                    (ApprovalProcess.document_type_id == int(parameters['document_type_id'])) &
                    (ApprovalProcess.entity_iin == parameters['entity_iin']))

    result = await database.execute(query)
    return apInstance



