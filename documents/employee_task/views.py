from certifi import where
from fastapi import HTTPException
from sqlalchemy import String, func, null, select, insert, tuple_, update, delete
from catalogs.approval_route.models import ApprovalRoute
from catalogs.approval_route.views import get_approval_routes_by_metadata
from catalogs.approval_status.models import ApprovalStatus
from catalogs.assignment_status.models import AssignmentStatus
from catalogs.enum_types.views import enum_document_type_fillDataFromDict, get_enum_document_type_id_by_metadata_name
from catalogs.user.models import User, user_fillDataFromDict
from core.db import database
from common_module.urls_module import correct_datetime, correct_datetime, is_need_filter

from documents.employee_task.models import EmployeeTask, EmployeeTaskOut
from catalogs.enum_types.models import EnumDocumentType
from catalogs.entity.models import Entity, entity_fillDataFromDict


async def get_employee_task_by_id(employee_task_id: int, **kwargs):
    if(kwargs['nested']):
        return await get_employee_task_nested_by_id(employee_task_id, **kwargs)
    
    employee_task_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("employee_task")
    query = select(EmployeeTask).where(EmployeeTask.id == employee_task_id).\
            where(EmployeeTask.enum_document_type_id == employee_task_enum_document_type_id)
    
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(EmployeeTask.entity_iin.in_(kwargs['entity_iin_list']))

    result = await database.fetch_one(query)
    if result == None:
        raise HTTPException(status_code=404, detail="Item not found") 
    resultEmployeeTask = dict(result)
    return resultEmployeeTask

async def get_employee_task_count(**kwargs):
    employee_task_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("employee_task")
    query = select(func.count(EmployeeTask.id)).where(EmployeeTask.enum_document_type_id == employee_task_enum_document_type_id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(EmployeeTask.entity_iin.in_(kwargs['entity_iin_list']))
    return await database.execute(query)

async def get_employee_task_nested_by_id(employee_task_id: int, **kwargs):
    employee_task_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("employee_task")
    query = select(
                EmployeeTask,
                Entity.name.label("entity_name"),
                Entity.iin.label("entity_iin"),
                Entity.id.label("entity_id"),
                User.id.label("user_id"),
                User.name.label("user_name"),
                User.email.label("user_email"),
                EnumDocumentType.name.label("enum_document_type_name"),
                EnumDocumentType.description.label("enum_document_type_description")).\
                join(AssignmentStatus, (EmployeeTask.id == AssignmentStatus.document_id) & 
                    (EmployeeTask.enum_document_type_id == AssignmentStatus.enum_document_type_id) & (AssignmentStatus.is_active), isouter=True).\
                join(User, EmployeeTask.author_id == User.id, isouter=True).\
                join(Entity, EmployeeTask.entity_iin == Entity.iin, isouter=True).\
                join(EnumDocumentType, EmployeeTask.enum_document_type_id == EnumDocumentType.id, isouter=True).\
                where(EmployeeTask.id == employee_task_id).\
                where(EmployeeTask.enum_document_type_id == employee_task_enum_document_type_id)       
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(EmployeeTask.entity_iin.in_(kwargs['entity_iin_list']))
    result = await database.fetch_one(query)

    if(is_need_filter('include_approve_route', kwargs)):
        kwargs['employee_task_id'] = employee_task_id
        routes_result  = await get_approval_routes_by_metadata('employee_task', **kwargs)
        include_approve_route = True
    else:
        include_approve_route = False

    if result == None:
        raise HTTPException(status_code=404, detail="Item not found") 

    recordDict = dict(result)
    recordDict['entity'] = entity_fillDataFromDict(recordDict)
    recordDict['enum_document_type'] = enum_document_type_fillDataFromDict(recordDict)
    recordDict['author'] = user_fillDataFromDict(recordDict)
    
    if(include_approve_route):
            if recordDict['approval_process_id'] in routes_result:
                recordDict['current_approval_routes'] = routes_result[recordDict['approval_process_id']]['current_approval_routes']
                recordDict['all_approval_routes'] = routes_result[recordDict['approval_process_id']]['all_approval_routes']
            else:
                recordDict['current_approval_routes'] = []
                recordDict['all_approval_routes'] = []

    return recordDict

async def delete_employee_task_by_id(employee_task_id: int, **kwargs):
    query = delete(EmployeeTask).where(EmployeeTask.id == employee_task_id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(EmployeeTask.entity_iin.in_(kwargs['entity_iin_list']))
    resultEmployeeTask = await database.execute(query)

    return resultEmployeeTask

async def get_employee_task_list(limit: int = 100, skip: int = 0, **kwargs)->list[EmployeeTaskOut]:
    employee_task_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("employee_task")
    if(kwargs['nested']):
        return await get_employee_task_nested_list(limit, skip, **kwargs)

    query = select( 
                EmployeeTask.id, 
                EmployeeTask.guid, 
                EmployeeTask.number, 
                EmployeeTask.date, 
                EmployeeTask.comment, 
                EmployeeTask.enum_document_type_id, 
                EmployeeTask.entity_iin,
                EmployeeTask.author_id).\
                join(AssignmentStatus, (EmployeeTask.id == AssignmentStatus.document_id) & 
                    (EmployeeTask.enum_document_type_id == AssignmentStatus.enum_document_type_id) & (AssignmentStatus.is_active), isouter=True).\
                where(EmployeeTask.enum_document_type_id == employee_task_enum_document_type_id).\
                order_by(EmployeeTask.id).limit(limit).offset(skip)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(EmployeeTask.entity_iin.in_(kwargs['entity_iin_list']))

    if('include_approve_route' in kwargs and kwargs['include_approve_route']):
        include_approve_route = True
        routes_result  = await get_approval_routes_by_metadata('employee_task', **kwargs)
    else:
        include_approve_route = False

    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        if(include_approve_route):
            if recordDict['approval_process_id'] in routes_result:
                recordDict['current_approval_routes'] = routes_result[recordDict['approval_process_id']]['current_approval_routes']
                recordDict['all_approval_routes'] = routes_result[recordDict['approval_process_id']]['all_approval_routes']
            else:
                recordDict['current_approval_routes'] = []
                recordDict['all_approval_routes'] = []
        listValue.append(recordDict)
    return listValue

async def get_employee_task_nested_list(limit: int = 100, skip: int = 0, **kwargs)->list[EmployeeTaskOut]:
    employee_task_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("employee_task")
    query = select( 
                EmployeeTask.id, 
                EmployeeTask.guid, 
                EmployeeTask.number, 
                EmployeeTask.date, 
                EmployeeTask.comment, 
                EmployeeTask.enum_document_type_id.label('enum_document_type_id'), 
                EmployeeTask.entity_iin.label('entity_iin'),
                Entity.name.label("entity_name"),
                Entity.id.label("entity_id"),
                User.id.label("user_id"),
                User.name.label("user_name"),
                User.email.label("user_email"),
                EnumDocumentType.name.label("enum_document_type_name"),
                EnumDocumentType.description.label("enum_document_type_description")).\
                join(Entity, EmployeeTask.entity_iin == Entity.iin, isouter=True).\
                join(User, EmployeeTask.author_id == User.id, isouter=True).\
                join(EnumDocumentType, EmployeeTask.enum_document_type_id == EnumDocumentType.id, isouter=True).\
                join(AssignmentStatus, (EmployeeTask.id == AssignmentStatus.document_id) & 
                    (EmployeeTask.enum_document_type_id == AssignmentStatus.enum_document_type_id) & (AssignmentStatus.is_active), isouter=True).\
                where(EmployeeTask.enum_document_type_id == employee_task_enum_document_type_id).\
                    order_by(EmployeeTask.id)
               
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(EmployeeTask.entity_iin.in_(kwargs['entity_iin_list']))

    records = await database.fetch_all(query)
    listValue = []
    
    if (len(records) == 0):
        return listValue
    
    if('include_approve_route' in kwargs and kwargs['include_approve_route']):
        include_approve_route = True
        routes_result  = await get_approval_routes_by_metadata('employee_task', **kwargs)
    else:
        include_approve_route = False

    for rec in records:
        recordDict = dict(rec)
        recordDict['entity'] = entity_fillDataFromDict(rec)
        recordDict['enum_document_type'] = enum_document_type_fillDataFromDict(rec)
        recordDict['author'] = user_fillDataFromDict(rec)
        if(include_approve_route):
            if recordDict['approval_process_id'] in routes_result:
                recordDict['current_approval_routes'] = routes_result[recordDict['approval_process_id']]['current_approval_routes']
                recordDict['all_approval_routes'] = routes_result[recordDict['approval_process_id']]['all_approval_routes']
            else:
                recordDict['current_approval_routes'] = []
                recordDict['all_approval_routes'] = []
        listValue.append(recordDict)
    return listValue


    
async def get_max_employee_task_number(entity_iin: str)->str:
    query = select(func.max(EmployeeTask.number).label('number')).where(EmployeeTask.entity_iin == entity_iin)
    result = await database.fetch_one(query)
    
    if result == None or result['number'] == null or result['number'] == None:
        number = 1
    else:
        number = ''.join(filter(str.isdigit, result['number']))
        number = int(number) + 1

    return str(number)

async def post_employee_task(purchaseRequisitionInstance : dict, **kwargs):
    # RLS
    if(is_need_filter('entity_iin_list', kwargs) and purchaseRequisitionInstance["entity_iin"] not in kwargs['entity_iin_list']):
        raise HTTPException(status_code=403, detail="Forbidden")

    employee_task_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("employee_task")

    purchaseRequisitionInstance["date"] = correct_datetime(purchaseRequisitionInstance["date"])
    max_number = await get_max_employee_task_number(purchaseRequisitionInstance["entity_iin"])
    query = insert(EmployeeTask).values(
                guid = purchaseRequisitionInstance["guid"], 
                number = max_number, 
                date = purchaseRequisitionInstance["date"],
                comment = purchaseRequisitionInstance["comment"], 
                enum_document_type_id = employee_task_enum_document_type_id, 
                author_id = kwargs['current_user']['id'],
                entity_iin = purchaseRequisitionInstance["entity_iin"])

    newEmployeeTaskId = await database.execute(query)
    return {**purchaseRequisitionInstance, 'id': newEmployeeTaskId}

async def update_employee_task(purchaseRequisitionInstance: dict, purchaseRequisitionId: int, **kwargs):
    purchaseRequisitionInstance["date"] = correct_datetime(purchaseRequisitionInstance["date"])
    employee_task_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("employee_task")

    query = update(EmployeeTask).values(
                number = purchaseRequisitionInstance["number"], 
                date = purchaseRequisitionInstance["date"],
                comment = purchaseRequisitionInstance["comment"], 
                enum_document_type_id = employee_task_enum_document_type_id, 
                author_id = kwargs['current_user']['id'],
                guid = purchaseRequisitionInstance["guid"]).where(
                    (EmployeeTask.id == purchaseRequisitionId) & 
                    (EmployeeTask.entity_iin == purchaseRequisitionInstance["entity_iin"]))
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(EmployeeTask.entity_iin.in_(kwargs['entity_iin_list']))

    result = await database.execute(query)
    return purchaseRequisitionInstance

