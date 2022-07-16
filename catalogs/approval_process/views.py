import asyncio
from datetime import date
from fastapi import HTTPException
from sqlalchemy import String, Table, func, select, insert, update, delete, event, table
from catalogs.approval_route.models import ApprovalRoute
from catalogs.approval_status.models import ApprovalStatus
from catalogs.enum_types.views import enum_document_type_fillDataFromDict
from common_module.approve_module import notificate_user_by_approval_process_id
from common_module.urls_module import is_need_filter
from core.db import database
from documents.purchase_requisition.models import PurchaseRequisition

from catalogs.approval_process.models import ApprovalProcess
from catalogs.approval_template.models import ApprovalTemplate, approval_template_fillDataFromDict
from catalogs.approval_template_step.models import ApprovalTemplateStep
from catalogs.approval_template_step.views import get_approval_template_step_list
from catalogs.approval_route.views import delete_approval_routes_by_approval_process_id, get_approval_route_by_aproval_process_id,\
                 post_approval_routes_by_approval_process_id, get_approval_route_nested_by_aproval_process_id, update_approval_routes_by_approval_process_id
from catalogs.enum_types.models import EnumDocumentType
from catalogs.entity.models import Entity, entity_fillDataFromDict
from documents.purchase_requisition.views import get_purchase_requisition_nested_by_id

async def collectRoutes(list_of_object: list, approval_process_id):
    listDict = []
    for item in list_of_object:
        itemDict = dict(item)
        # itemDict['type'] = 'line' if itemDict['type'] == EnumStepType.line else 'paralel'
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

async def delete_approval_process_by_id(approval_process_id: int, **kwargs):
    
    resultDelete = await delete_approval_routes_by_approval_process_id(approval_process_id)
    query = delete(ApprovalProcess).where(ApprovalProcess.id == approval_process_id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(ApprovalProcess.entity_iin.in_(kwargs['entity_iin_list']))
    return await database.execute(query)

async def get_approval_process_list(limit: int = 100,skip: int = 0,**kwargs):

    if(kwargs['nested']):
        return await get_approval_process_nested_list(limit, skip, **kwargs)

    query = select(ApprovalProcess).limit(limit).offset(skip).\
                where((ApprovalProcess.is_active))
    if('id' in kwargs and kwargs['id']):
        query = query.where(ApprovalProcess.id == int(kwargs['id']))
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(ApprovalProcess.entity_iin.in_(kwargs['entity_iin_list']))

    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def get_approval_process_nested_list(limit: int = 100,skip: int = 0, **kwargs):
    # Будем делать Union all, потому как левое соединение со всеми таблицами рождает нагрузку на субд
    query_AR = select(ApprovalProcess,
                    PurchaseRequisition.number.label('number'),
                    PurchaseRequisition.date.label('date'),
                    EnumDocumentType.description.label('enum_document_type_description'),
                    EnumDocumentType.name.label('enum_document_type_name'),
                    ApprovalTemplate.name.label('approval_template_name'),
                    ApprovalTemplate.id.label('approval_template_id'),
                    Entity.name.label("entity_name"),
                    Entity.iin.label("entity_iin"),
                    Entity.id.label("entity_id")).\
                join(ApprovalProcess, ((PurchaseRequisition.id == ApprovalProcess.document_id) & (PurchaseRequisition.enum_document_type_id == ApprovalProcess.enum_document_type_id))).\
                join(ApprovalTemplate, (ApprovalTemplate.id == ApprovalProcess.approval_template_id)).\
                join(Entity, (Entity.iin == ApprovalProcess.entity_iin)).\
                join(EnumDocumentType, (EnumDocumentType.id == ApprovalProcess.enum_document_type_id)).\
                where(ApprovalProcess.is_active).\
                limit(limit).offset(skip)
    if('id' in kwargs and kwargs['id']):
        query_AR = query_AR.where(ApprovalProcess.id == int(kwargs['id']))
    # query = query_purchase_requisition.union_all(select2).alias('pr_list')
    query = query_AR

    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(ApprovalProcess.entity_iin.in_(kwargs['entity_iin_list']))

    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['enum_document_type'] = enum_document_type_fillDataFromDict(recordDict)
        recordDict['document'] = {'number': recordDict['number'], 'date': recordDict['date']}
        recordDict['entity'] = entity_fillDataFromDict(recordDict)
        recordDict['approval_template'] = approval_template_fillDataFromDict(recordDict)
        listValue.append(recordDict)
    return listValue

async def post_approval_process(apInstance : dict, **kwargs):
    # RLS
    if(is_need_filter('entity_iin_list', kwargs) and apInstance["entity_iin"] not in kwargs['entity_iin_list']):
        raise HTTPException(status_code=403, detail="Forbidden")

    query = insert(ApprovalProcess).values(
                is_active = apInstance["is_active"], 
                document_id = int(apInstance["document_id"]),
                enum_document_type_id = int(apInstance["enum_document_type_id"]),
                entity_iin = apInstance["entity_iin"],
                approval_template_id = int(apInstance["approval_template_id"]),
                start_date = apInstance["start_date"],
                end_date = apInstance["end_date"],
                status = apInstance["status"])
    result = await database.execute(query)
    routesResult = await post_approval_routes_by_approval_process_id(await collectRoutes(apInstance['routes'], result))
    return {**apInstance, 'id': result}

async def update_approval_process(approval_process_id: int, apInstance: dict, **kwargs):

    query = update(ApprovalProcess).values(
                is_active = apInstance["is_active"], 
                document_id = int(apInstance["document_id"]),
                enum_document_type_id = int(apInstance["enum_document_type_id"]),
                entity_iin = apInstance["entity_iin"],
                approval_template_id = int(apInstance["approval_template_id"]),
                start_date = apInstance["start_date"],
                end_date = apInstance["end_date"],
                status = apInstance["status"]).\
                    where(ApprovalProcess.id == approval_process_id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(ApprovalProcess.entity_iin.in_(kwargs['entity_iin_list']))

    result = await database.execute(query)
    routesResult = await update_approval_routes_by_approval_process_id(await collectRoutes(apInstance['routes'], approval_process_id), approval_process_id)
    return apInstance

async def start_approval_process(parameters, **kwargs):
    
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
                                        'enum_document_type_id': approval_processes['enum_document_type_id'],
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
                where((ApprovalTemplate.entity_iin == parameters['entity_iin']) & (ApprovalTemplate.enum_document_type_id == parameters['enum_document_type_id'])).limit(1)
    
    approval_template = await database.fetch_one(query)
    if approval_template == None:
        responseMap['Error'] = True
        responseMap['Text'] = 'Не найден шаблон согласования по документу'
        return responseMap

    responseMap['ApprovalTemplate'] = {'id': approval_template['id'], 'name': approval_template['name']}

    # Дальше ищем его шаги
    query = select(ApprovalTemplateStep.user_id, ApprovalTemplateStep.level, ApprovalTemplateStep.type).\
            where(ApprovalTemplateStep.approval_template_id == approval_template['id']).order_by(ApprovalTemplateStep.level, ApprovalTemplateStep.type)
    _qp_select_list = {'nested': False}
    approval_template_steps = await get_approval_template_step_list(approval_template['id'], **_qp_select_list)
    if len(approval_template_steps) == 0:
        responseMap['Error'] = True
        responseMap['Text'] = 'Не настроены шаги согласования в шаблоне'
        return responseMap

    # Есть запущенный процесс согласования, так что уходит отсюда
    # а то что уходиv только сейчас, выше нужно было создать информацию по шаблону согласования и шагаъ его
    if process_started and responseMap['Error']:
        return responseMap

    # декативируем старые процессы
    query = update(ApprovalProcess).values(
                    is_active = False).\
                where(
                    (ApprovalProcess.is_active) &
                    (ApprovalProcess.document_id == int(parameters['document_id'])) &
                    (ApprovalProcess.enum_document_type_id == int(parameters['enum_document_type_id'])) &
                    (ApprovalProcess.entity_iin == parameters['entity_iin']))

    result = await database.execute(query)
   
    # ------------------------------ СОЗДАНИЕ ПРОЦЕССА -------------------------------
        

    # Создаем шаги согласования
    listRoutes = []
    for item in approval_template_steps:
        rout_step = {
            'is_active': True,
            'level': item['level'],
            'type': item['type'],
            'document_id': parameters['document_id'],
            'enum_document_type_id': parameters['enum_document_type_id'],
            'entity_iin': parameters['entity_iin'],
            'user_id': item['user_id'],
            'approval_template_id': approval_template['id'],
            'approval_process_id': 0,
            'hash': '',
        }
        listRoutes.append(rout_step) 

    # если все норм то создаем сам процесс
    apInstance = {
        'is_active': True,
        'document_id': parameters['document_id'],
        'enum_document_type_id': parameters['enum_document_type_id'],
        'entity_iin': parameters['entity_iin'],
        'approval_template_id': approval_template['id'],
        'status': 'в работе',
        'start_date': date.today(),
        'end_date': None,
        'routes': listRoutes
    }

    responseMap['ApprovalProcess'] = await post_approval_process(apInstance, **kwargs)
    responseMap['ApprovalProcessStatus'] = "в работе"
    responseMap['Text'] = 'Процесс согласования запущен'
    responseMap['ApprovalRoute'] =  await get_approval_route_by_aproval_process_id(responseMap['ApprovalProcess']['id'])
    
    asyncio.create_task(check_approval_process(responseMap['ApprovalProcess']['id'], **kwargs))

    return responseMap

async def check_approval_process(approval_process_id, **kwargs):
    document_data = await get_document_data_by_approval_process_id(approval_process_id, **kwargs)
    
    if (document_data['metadata_name'].lower() == 'purchase_requisition'):
        document_full_data  = await get_purchase_requisition_nested_by_id(document_data['document_id'])
        kwargs = {
            'enum_document_type_description': document_full_data['enum_document_type_description'], 
            'number': document_full_data['number'],
            'date': document_full_data['date'],
            'meta_data_name': document_data['metadata_name'].lower()}

    await notificate_user_by_approval_process_id(approval_process_id, **kwargs)


async def check_approval_processes(parameters, **kwargs):
    
    responseMap = {}

    # Делаем массив
    if type(parameters['document_id']) is int:
        listId = [parameters['document_id']]
    else: 
        listId = parameters['document_id'] 

    query = select( 
            ApprovalProcess.document_id,
            ApprovalProcess.enum_document_type_id, 
            ApprovalProcess.entity_iin,
            ApprovalProcess.approval_template_id,
            ApprovalProcess.status,
            ApprovalProcess.is_active,
            ApprovalProcess.start_date,
            ApprovalProcess.end_date,
            func.max(ApprovalProcess.id).label('id')).\
                where((ApprovalProcess.is_active) &
                    (ApprovalProcess.entity_iin == parameters['entity_iin']) & 
                    (ApprovalProcess.document_id.in_(listId)) & 
                    (ApprovalProcess.enum_document_type_id == parameters['enum_document_type_id'])).\
                group_by(ApprovalProcess.entity_iin, 
                        ApprovalProcess.enum_document_type_id,
                        ApprovalProcess.approval_template_id, 
                        ApprovalProcess.status,
                        ApprovalProcess.document_id,
                        ApprovalProcess.is_active,
                        ApprovalProcess.start_date,
                        ApprovalProcess.end_date,)

    result = await database.fetch_all(query)

    if len(result)>0:
        for item in result:
            responseMap[item['document_id']] = dict(item)

    
    return responseMap

async def is_approval_process_finished(parameters, **kwargs):

    query_route = select( 
                    ApprovalProcess.id.label("approval_process_id"),
                    ApprovalProcess.status.label("approval_process_status"),
                    func.count(ApprovalRoute.id).label("status_count"),
                    func.lower("all_routes", type_= String).label("status"),).\
                    join(ApprovalRoute, (ApprovalProcess.id == ApprovalRoute.approval_process_id) & (ApprovalRoute.is_active), isouter=True).\
                    where(
                    (ApprovalProcess.is_active) &
                    (ApprovalProcess.status == 'в работе') &
                    (ApprovalProcess.document_id == int(parameters['document_id'])) &
                    (ApprovalProcess.enum_document_type_id == int(parameters['enum_document_type_id'])) &
                    (ApprovalProcess.entity_iin == parameters['entity_iin'])).\
                    group_by(ApprovalProcess.id, ApprovalProcess.status)

    query_status = select( 
                    ApprovalProcess.id,
                    ApprovalProcess.status,
                    func.count(ApprovalStatus.status),
                    ApprovalStatus.status).\
                    join(ApprovalRoute, (ApprovalProcess.id == ApprovalRoute.approval_process_id) & (ApprovalRoute.is_active), isouter=True).\
                    join(ApprovalStatus, (ApprovalRoute.id == ApprovalStatus.approval_route_id) & (ApprovalStatus.is_active), isouter=True).\
                    where(
                    (ApprovalProcess.is_active) &
                    (ApprovalProcess.status == 'в работе') &
                    (ApprovalProcess.document_id == int(parameters['document_id'])) &
                    (ApprovalProcess.enum_document_type_id == int(parameters['enum_document_type_id'])) &
                    (ApprovalProcess.entity_iin == parameters['entity_iin']) &
                    (ApprovalStatus.status != None)).\
                    group_by(ApprovalProcess.id, ApprovalProcess.status, ApprovalStatus.status)
                    

    query = query_route.union_all(query_status).alias('approval_route_list')
    result = await database.fetch_all(query)
    approved_procesess = {}
    
    for item in result:
        item_row = dict(item)

        if item_row['approval_process_id'] not in approved_procesess:
            approved_procesess[item_row['approval_process_id']] = {'routes_count': 0, 'id': item_row['approval_process_id'], 'rejected': False, 'approved': False}

        if approved_procesess[item_row['approval_process_id']]['rejected'] or \
            approved_procesess[item_row['approval_process_id']]['approved']:
            continue

        if item_row['status'] == 'all_routes' and item_row['status_count']>0:
            approved_procesess[item_row['approval_process_id']]['routes_count'] = item_row['status_count']
        elif (item_row['status'] == 'отклонен' and item_row['status_count']>0):
            await set_approval_process_status(item_row['approval_process_id'], 'отклонен', **kwargs)
            approved_procesess[item_row['approval_process_id']]['rejected'] = True
            continue
        elif (item_row['status'] == 'согласован' and item_row['status_count']>0 and \
            approved_procesess[item_row['approval_process_id']]['routes_count']>0 and \
            approved_procesess[item_row['approval_process_id']]['routes_count'] == item_row['status_count']):
            await set_approval_process_status(item_row['approval_process_id'], 'подписан', **kwargs)
            approved_procesess[item_row['approval_process_id']]['approved'] = True
    
    return approved_procesess

async def cancel_approval_process(parameters, **kwargs):
    
    apInstance = {
        'is_active': False,
        'document_id': parameters['document_id'],
        'enum_document_type_id': parameters['enum_document_type_id'],
        'entity_iin': parameters['entity_iin']
        }

    query = update(ApprovalProcess).values(
                    is_active = False, 
                    status = "отменен",
                    end_date = date.today()).\
                where(
                    (ApprovalProcess.is_active) &
                    (ApprovalProcess.document_id == int(parameters['document_id'])) &
                    (ApprovalProcess.enum_document_type_id == int(parameters['enum_document_type_id'])) &
                    (ApprovalProcess.entity_iin == parameters['entity_iin']))

    result = await database.execute(query)
    return apInstance

async def set_approval_process_status(approval_process_id: int, approval_process_status: str, **kwargs):
    
    query = update(ApprovalProcess).values(
                    status = approval_process_status,
                    end_date = date.today()).\
                where(ApprovalProcess.id == approval_process_id)

    return await database.execute(query)

async def get_document_data_by_approval_process_id(approval_process_id: int, **kwargs):
    query = select( 
                    ApprovalProcess.id,
                    ApprovalProcess.document_id,
                    ApprovalProcess.enum_document_type_id,
                    EnumDocumentType.metadata_name,
                    EnumDocumentType.description).\
                    join(EnumDocumentType, (ApprovalProcess.enum_document_type_id == EnumDocumentType.id), isouter=True).\
                    where(
                    (ApprovalProcess.id == approval_process_id))
    result = await database.fetch_one(query)
    if result == None:
        raise HTTPException(status_code=404, detail="Item not found") 
    return dict(result)