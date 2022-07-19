from fastapi import HTTPException
from sqlalchemy import String, func, select, insert, tuple_, update, delete
from datetime import datetime
from sqlalchemy.orm import aliased

from catalogs.enum_types.views import get_enum_document_type_id_by_metadata_name
from common_module.urls_module import is_need_filter, is_key_exist

from core.db import database

from catalogs.task_status.models import TaskStatus
from catalogs.user.models import User, fill_assigned_user_data_from_dict, fill_author_data_from_dict

async def get_task_status_by_id(task_status_id: int, **kwargs):
    query = select(TaskStatus).where(TaskStatus.id == task_status_id)
    result = await database.fetch_one(query)
    return result

async def get_task_status_nested_by_id(aproval_status_id: int, **kwargs):
    UserT = aliased(User)
    UserAssignedT = aliased(User)
    query = select(TaskStatus,
            UserT.id.label('author_id'),
            UserT.email.label('author_email'),
            UserT.name.label('author_name'),
            UserAssignedT.id.label('assigned_user_id'),
            UserAssignedT.email.label('assigned_user_email'),
            UserAssignedT.name.label('assigned_user_name')).\
            join(UserT, TaskStatus.author_id == UserT.id, isouter=True).\
            join(UserAssignedT, TaskStatus.assigned_user_id == UserAssignedT.id, isouter=True).\
            where(TaskStatus.id == aproval_status_id)
    records = await database.fetch_one(query)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(TaskStatus.entity_iin.in_(kwargs['entity_iin_list']))

    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['author'] = fill_author_data_from_dict(recordDict)
        recordDict['assigned_user'] = fill_assigned_user_data_from_dict(recordDict)
        listValue.append(recordDict)
    return listValue

async def delete_task_status_by_id(task_status_list_id: list, **kwargs):
    query = delete(TaskStatus).where(TaskStatus.id.in_(task_status_list_id))
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(TaskStatus.entity_iin.in_(kwargs['entity_iin_list']))
    result = await database.execute(query)
    return result

async def get_task_status_list(limit: int = 100,skip: int = 0,**kwargs):

    query = select(TaskStatus).limit(limit).offset(skip)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(TaskStatus.entity_iin.in_(kwargs['entity_iin_list']))

    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def post_task_status(asInstance : dict, **kwargs):

    if(is_need_filter('entity_iin_list', kwargs) and asInstance["entity_iin"] not in kwargs['entity_iin_list']):
        raise HTTPException(status_code=403, detail="Forbidden")

    query = update(TaskStatus).values(
                is_active = False).\
                where((TaskStatus.document_id == int(asInstance["document_id"])) &
                (TaskStatus.enum_document_type_id == int(asInstance["enum_document_type_id"])) &
                (TaskStatus.entity_iin == asInstance["entity_iin"]) &
                (TaskStatus.is_active == True ))

    result = await database.execute(query)

    query = insert(TaskStatus).values(
                is_active = asInstance["is_active"], 
                status = asInstance["status"],
                document_id = int(asInstance["document_id"]),
                date = datetime.now(),
                comment = asInstance["comment"],
                enum_document_type_id = int(asInstance["enum_document_type_id"]),
                entity_iin = asInstance["entity_iin"],
                author_id = int(kwargs['current_user']['id']),
                assigned_user_id = int(asInstance["assigned_user_id"]))

    result = await database.execute(query)

    return {**asInstance, 'id': result, 'author_id': kwargs['current_user']['id']}
    

async def update_task_status(asInstance: dict, task_status_id: int, **kwargs):

    query = update(TaskStatus).values(
                is_active = asInstance["is_active"], 
                status = asInstance["status"],
                document_id = int(asInstance["document_id"]),
                date = datetime.now(),
                comment = asInstance["comment"],
                enum_document_type_id = int(asInstance["enum_document_type_id"]),
                entity_iin = asInstance["entity_iin"],
                author_id = int(kwargs['current_user']['id']),
                assigned_user_id = int(asInstance["assigned_user_id"])).\
                    where(TaskStatus.id == task_status_id)

    result = await database.execute(query)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(TaskStatus.entity_iin.in_(kwargs['entity_iin_list']))
    return asInstance

async def get_task_status_by_metadata(metadata_name: str, **kwargs):
    
    metadata_name_enum_document_type_id = await get_enum_document_type_id_by_metadata_name(metadata_name)
    query_min = select(func.max(TaskStatus.id).label("max_id"),
                        TaskStatus.document_id).\
                    where((TaskStatus.is_active) & (TaskStatus.enum_document_type_id == metadata_name_enum_document_type_id)).\
                    group_by(TaskStatus.document_id)
                    
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query_min = query_min.where(TaskStatus.entity_iin.in_(kwargs['entity_iin_list']))

    if(is_key_exist('document_id', kwargs)):
        query_min = query_min.where(TaskStatus.document_id.in_(kwargs['document_id']))

    UserT = aliased(User)
    UserAssignedT = aliased(User)

    query_current_task_status = select(
            func.lower("last_task_status", type_= String).label('query_type'), 
            TaskStatus.id,
            TaskStatus.document_id,
            TaskStatus.comment,
            TaskStatus.date,
            TaskStatus.entity_iin,
            TaskStatus.author_id,
            TaskStatus.status,
            TaskStatus.enum_document_type_id,
            UserT.id.label('author_id'),
            UserT.email.label('author_email'),
            UserT.name.label('author_name'),
            UserAssignedT.id.label('assigned_user_id'),
            UserAssignedT.email.label('assigned_user_email'),
            UserAssignedT.name.label('assigned_user_name')).\
            join(UserT, (TaskStatus.author_id == UserT.id), isouter=True).\
            join(UserAssignedT, (TaskStatus.assigned_user_id == UserAssignedT.id), isouter=True).\
            where((TaskStatus.is_active)  & (TaskStatus.enum_document_type_id == metadata_name_enum_document_type_id)).\
            where(tuple_(TaskStatus.id, TaskStatus.document_id).in_(query_min))
    

    query_all_task_status = select(
            func.lower("all_task_status", type_= String).label('query_type'), 
            TaskStatus.id,
            TaskStatus.document_id,
            TaskStatus.comment,
            TaskStatus.date,
            TaskStatus.entity_iin,
            TaskStatus.author_id,
            TaskStatus.status,
            TaskStatus.enum_document_type_id,
            UserT.id.label('author_id'),
            UserT.email.label('author_email'),
            UserT.name.label('author_name'),
            UserAssignedT.id.label('assigned_user_id'),
            UserAssignedT.email.label('assigned_user_email'),
            UserAssignedT.name.label('assigned_user_name')).\
            join(UserT, (TaskStatus.author_id == UserT.id), isouter=True).\
            join(UserAssignedT, (TaskStatus.assigned_user_id == UserAssignedT.id), isouter=True).\
            where((TaskStatus.enum_document_type_id == metadata_name_enum_document_type_id))
            
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query_all_task_status = query_all_task_status.where(TaskStatus.entity_iin.in_(kwargs['entity_iin_list']))

    if(is_key_exist('document_id', kwargs)):
        query_min = query_min.where(TaskStatus.document_id.in_(kwargs['document_id']))
    
    query = query_current_task_status.union_all(query_all_task_status).alias('task_status_list')   
    
    records = await database.fetch_all(query)
    dictValue = {}
    
    for rec in records:
        recordDict = dict(rec)
        if(recordDict['document_id'] not in dictValue):
            dictValue[recordDict['document_id']] = {'last_task_status': {}, 'all_task_status': []}
        
        if(recordDict['query_type']=='last_task_status'):
            dictValue[recordDict['document_id']]['last_task_status'] = recordDict
        elif(recordDict['query_type']=='all_task_status'):
            dictValue[recordDict['document_id']]['all_task_status'].append(recordDict)
        
    return dictValue
