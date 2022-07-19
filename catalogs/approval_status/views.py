import asyncio
from multiprocessing.sharedctypes import Value
from sqlalchemy import select, insert, update, delete
from datetime import datetime
from catalogs.approval_process.views import check_approval_process, is_approval_process_finished

from core.db import database

from catalogs.approval_status.models import ApprovalStatus
from catalogs.user.models import User, fill_user_data_from_dict

async def get_approval_status_by_id(approval_status_id: int):
    query = select(ApprovalStatus).where(ApprovalStatus.id == approval_status_id)
    result = await database.fetch_one(query)
    return result

async def get_approval_status_nested_by_id(aproval_status_id: int):
    query = select(ApprovalStatus,
            User.id.label('user_id'),
            User.email.label('user_email'),
            User.name.label('user_name')).\
            join(User, ApprovalStatus.user_id == User.id, isouter=True).\
            where(ApprovalStatus.id == aproval_status_id)
    records = await database.fetch_one(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['user'] = fill_user_data_from_dict(recordDict)
        listValue.append(recordDict)
    return listValue

async def delete_approval_status_by_id(approval_status_list_id: list):
    query = delete(ApprovalStatus).where(ApprovalStatus.id.in_(approval_status_list_id))
    result = await database.execute(query)
    return result

async def get_approval_status_list(limit: int = 100,skip: int = 0,**kwargs):

    query = select(ApprovalStatus).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def post_approval_status(asInstance : dict):

    query = update(ApprovalStatus).values(
                is_active = False, 
                date = datetime.now()).\
                    where((ApprovalStatus.enum_document_type_id == int(asInstance["enum_document_type_id"])) & 
                            (ApprovalStatus.approval_route_id == int(asInstance["approval_route_id"])) &
                            (ApprovalStatus.entity_iin == asInstance["entity_iin"]) &
                            (ApprovalStatus.user_id == int(asInstance["user_id"])))

    result = await database.execute(query)
    
    query = insert(ApprovalStatus).values(
                is_active = asInstance["is_active"], 
                status = asInstance["status"],
                document_id = int(asInstance["document_id"]),
                date = datetime.now(),
                comment = asInstance["comment"],
                enum_document_type_id = int(asInstance["enum_document_type_id"]),
                approval_route_id = int(asInstance["approval_route_id"]),
                entity_iin = asInstance["entity_iin"],
                user_id = int(asInstance["user_id"]))

    result = await database.execute(query)

    approval_processes = await is_approval_process_finished(parameters = asInstance)
    for key in approval_processes:
        if (approval_processes[key]['rejected']!=True and approval_processes[key]['approved']!=True):
            asyncio.create_task(check_approval_process(key))
    return {**asInstance, 'id': result}
    

async def update_approval_status(asInstance: dict, approval_status_id: int):

    query = update(ApprovalStatus).values(
                is_active = asInstance["is_active"], 
                status = asInstance["status"],
                document_id = int(asInstance["document_id"]),
                date = datetime.now(),
                comment = asInstance["comment"],
                enum_document_type_id = int(asInstance["enum_document_type_id"]),
                approval_route_id = int(asInstance["approval_route_id"]),
                entity_iin = asInstance["entity_iin"],
                user_id = int(asInstance["user_id"])).\
                    where(ApprovalStatus.id == approval_status_id)

    result = await database.execute(query)
    return asInstance
