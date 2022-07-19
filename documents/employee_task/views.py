from certifi import where
from fastapi import HTTPException
from sqlalchemy import String, func, null, select, insert, tuple_, update, delete
from catalogs.approval_route.models import ApprovalRoute
from catalogs.approval_route.views import get_approval_routes_by_metadata
from catalogs.approval_status.models import ApprovalStatus
from catalogs.task_status.models import TaskStatus
from catalogs.task_status.views import get_task_status_by_metadata
from catalogs.enum_types.views import enum_document_type_fill_data_from_dict, get_enum_document_type_id_by_metadata_name
from catalogs.user.models import User, fill_assigned_user_data_from_dict, fill_author_data_from_dict, fill_user_data_from_dict
from core.db import database
from sqlalchemy.orm import aliased
from common_module.urls_module import correct_datetime, correct_datetime, is_need_filter, is_key_exist

from documents.employee_task.models import EmployeeTask, EmployeeTaskOut
from catalogs.enum_types.models import EnumDocumentType
from catalogs.entity.models import Entity, entity_fill_data_from_dict


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
    UserT = aliased(User)
    UserAssignedT = aliased(User)
    query = select(
                EmployeeTask,
                Entity.name.label("entity_name"),
                Entity.iin.label("entity_iin"),
                Entity.id.label("entity_id"),
                UserT.id.label("author_id"),
                UserT.name.label("author_name"),
                UserT.email.label("author_email"),
                UserAssignedT.id.label("assigned_user_id"),
                UserAssignedT.name.label("assigned_user_name"),
                UserAssignedT.email.label("assigned_user_email"),
                TaskStatus.status.label("status"),
                TaskStatus.date.label("status_date"),
                TaskStatus.comment.label("status_comment"),
                EnumDocumentType.name.label("enum_document_type_name"),
                EnumDocumentType.description.label("enum_document_type_description")).\
                join(TaskStatus, (EmployeeTask.id == TaskStatus.document_id) & 
                    (EmployeeTask.enum_document_type_id == TaskStatus.enum_document_type_id) & (TaskStatus.is_active), isouter=True).\
                join(UserT, EmployeeTask.author_id == UserT.id, isouter=True).\
                join(UserAssignedT, TaskStatus.assigned_user_id == UserAssignedT.id, isouter=True).\
                join(Entity, EmployeeTask.entity_iin == Entity.iin, isouter=True).\
                join(EnumDocumentType, EmployeeTask.enum_document_type_id == EnumDocumentType.id, isouter=True).\
                where(EmployeeTask.id == employee_task_id).\
                where(EmployeeTask.enum_document_type_id == employee_task_enum_document_type_id)       
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(EmployeeTask.entity_iin.in_(kwargs['entity_iin_list']))
    result = await database.fetch_one(query)

    if result == None:
        raise HTTPException(status_code=404, detail="Item not found") 

    if(is_key_exist('include_task_status', kwargs)):
        kwargs['document_id'] = [employee_task_id]
        status_result  = await get_task_status_by_metadata('employee_task', **kwargs)
        include_task_status = True
    else:
        include_task_status = False

    recordDict = dict(result)
    recordDict['entity'] = entity_fill_data_from_dict(recordDict)
    recordDict['enum_document_type'] = enum_document_type_fill_data_from_dict(recordDict)
    recordDict['author'] = fill_author_data_from_dict(recordDict)
    recordDict['assigned_user'] = fill_assigned_user_data_from_dict(recordDict)

    if include_task_status:
        if employee_task_id in status_result:
            recordDict['last_task_status'] = status_result[employee_task_id]['last_task_status'] 
            recordDict['all_task_status'] = status_result[employee_task_id]['all_task_status']
        else:
            recordDict['last_task_status'] = [] 
            recordDict['all_task_status'] = []

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
                EmployeeTask.content,
                EmployeeTask.enum_document_type_id, 
                EmployeeTask.entity_iin,
                TaskStatus.status.label("status"),
                TaskStatus.date.label("status_date"),
                TaskStatus.comment.label("status_comment"),
                User.id.label("assigned_user_id"),
                User.name.label("assigned_user_name"),
                User.email.label("assigned_user_email"),
                EmployeeTask.author_id).\
                join(TaskStatus, (EmployeeTask.id == TaskStatus.document_id) & 
                    (EmployeeTask.enum_document_type_id == TaskStatus.enum_document_type_id) & (TaskStatus.is_active), isouter=True).\
                join(User, TaskStatus.assigned_user_id == User.id, isouter=True).\
                where(EmployeeTask.enum_document_type_id == employee_task_enum_document_type_id).\
                order_by(EmployeeTask.id).limit(limit).offset(skip)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(EmployeeTask.entity_iin.in_(kwargs['entity_iin_list']))

    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def get_employee_task_nested_list(limit: int = 100, skip: int = 0, **kwargs)->list[EmployeeTaskOut]:
    employee_task_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("employee_task")

    UserT = aliased(User)
    UserAssignedT = aliased(User)

    query = select( 
                EmployeeTask.id, 
                EmployeeTask.guid, 
                EmployeeTask.number, 
                EmployeeTask.date, 
                EmployeeTask.comment, 
                EmployeeTask.content,
                EmployeeTask.enum_document_type_id.label('enum_document_type_id'), 
                EmployeeTask.entity_iin.label('entity_iin'),
                Entity.name.label("entity_name"),
                Entity.id.label("entity_id"),
                UserT.id.label("author_id"),
                UserT.name.label("author_name"),
                UserT.email.label("author_email"),
                UserAssignedT.id.label("assigned_user_id"),
                UserAssignedT.name.label("assigned_user_name"),
                UserAssignedT.email.label("assigned_user_email"),
                TaskStatus.status.label("status"),
                TaskStatus.date.label("status_date"),
                TaskStatus.comment.label("status_comment"),
                EnumDocumentType.name.label("enum_document_type_name"),
                EnumDocumentType.description.label("enum_document_type_description")).\
                join(TaskStatus, (EmployeeTask.id == TaskStatus.document_id) & 
                    (EmployeeTask.enum_document_type_id == TaskStatus.enum_document_type_id) & (TaskStatus.is_active), isouter=True).\
                join(Entity, EmployeeTask.entity_iin == Entity.iin, isouter=True).\
                join(UserT, EmployeeTask.author_id == UserT.id, isouter=True).\
                join(UserAssignedT, TaskStatus.assigned_user_id == UserAssignedT.id, isouter=True).\
                join(EnumDocumentType, EmployeeTask.enum_document_type_id == EnumDocumentType.id, isouter=True).\
                where(EmployeeTask.enum_document_type_id == employee_task_enum_document_type_id).\
                    order_by(EmployeeTask.id)
               
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(EmployeeTask.entity_iin.in_(kwargs['entity_iin_list']))

    records = await database.fetch_all(query)
    listValue = []
    
    if (len(records) == 0):
        return listValue

    if(is_key_exist('include_task_status', kwargs)):
        status_result  = await get_task_status_by_metadata('employee_task', **kwargs)
        include_task_status = True
    else:
        include_task_status = False
    
    for rec in records:
        recordDict = dict(rec)
        recordDict['entity'] = entity_fill_data_from_dict(rec)
        recordDict['enum_document_type'] = enum_document_type_fill_data_from_dict(rec)
        recordDict['author'] = fill_author_data_from_dict(rec)
        recordDict['assigned_user'] = fill_assigned_user_data_from_dict(rec)
        if include_task_status:
            if recordDict['id'] in status_result:
                recordDict['last_task_status'] = status_result[recordDict['id']]['last_task_status'] 
                recordDict['all_task_status'] = status_result[recordDict['id']]['all_task_status']
            else:
                recordDict['last_task_status'] = {} 
                recordDict['all_task_status'] = []
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

async def post_employee_task(employeeTaskInstance : dict, **kwargs):
    # RLS
    if(is_need_filter('entity_iin_list', kwargs) and employeeTaskInstance["entity_iin"] not in kwargs['entity_iin_list']):
        raise HTTPException(status_code=403, detail="Forbidden")

    employee_task_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("employee_task")

    employeeTaskInstance["date"] = correct_datetime(employeeTaskInstance["date"])
    max_number = await get_max_employee_task_number(employeeTaskInstance["entity_iin"])
    query = insert(EmployeeTask).values(
                guid = employeeTaskInstance["guid"], 
                number = max_number, 
                date = employeeTaskInstance["date"],
                content = employeeTaskInstance["content"], 
                comment = employeeTaskInstance["comment"], 
                enum_document_type_id = employee_task_enum_document_type_id, 
                author_id = kwargs['current_user']['id'],
                entity_iin = employeeTaskInstance["entity_iin"])

    newEmployeeTaskId = await database.execute(query)
    return {**employeeTaskInstance, 'id': newEmployeeTaskId}

async def update_employee_task(employeeTaskInstance: dict, employeeTaskId: int, **kwargs):
    employeeTaskInstance["date"] = correct_datetime(employeeTaskInstance["date"])
    employee_task_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("employee_task")

    query = update(EmployeeTask).values(
                number = employeeTaskInstance["number"], 
                date = employeeTaskInstance["date"],
                content = employeeTaskInstance["content"], 
                comment = employeeTaskInstance["comment"], 
                enum_document_type_id = employee_task_enum_document_type_id, 
                # author_id = kwargs['current_user']['id'],
                guid = employeeTaskInstance["guid"]).where(
                    (EmployeeTask.id == employeeTaskId) & 
                    (EmployeeTask.entity_iin == employeeTaskInstance["entity_iin"]))
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(EmployeeTask.entity_iin.in_(kwargs['entity_iin_list']))

    result = await database.execute(query)
    return employeeTaskInstance

