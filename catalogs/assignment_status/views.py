import asyncio
from multiprocessing.sharedctypes import Value
from sqlalchemy import select, insert, update, delete
from datetime import datetime
from catalogs.approval_process.views import check_approval_process, is_approval_process_finished

from core.db import database

from catalogs.assignment_status.models import AssignmentStatus
from catalogs.user.models import User, user_fillDataFromDict

async def get_assignment_status_by_id(assignment_status_id: int):
    query = select(AssignmentStatus).where(AssignmentStatus.id == assignment_status_id)
    result = await database.fetch_one(query)
    return result

async def get_assignment_status_nested_by_id(aproval_status_id: int):
    query = select(AssignmentStatus,
            User.id.label('user_id'),
            User.email.label('user_email'),
            User.name.label('user_name')).\
            join(User, AssignmentStatus.user_id == User.id, isouter=True).\
            where(AssignmentStatus.id == aproval_status_id)
    records = await database.fetch_one(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['user'] = user_fillDataFromDict(recordDict)
        listValue.append(recordDict)
    return listValue

async def delete_assignment_status_by_id(assignment_status_list_id: list):
    query = delete(AssignmentStatus).where(AssignmentStatus.id.in_(assignment_status_list_id))
    result = await database.execute(query)
    return result

async def get_assignment_status_list(limit: int = 100,skip: int = 0,**kwargs):

    query = select(AssignmentStatus).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def post_assignment_status(asInstance : dict):

    query = update(AssignmentStatus).values(
                is_active = False, 
                date = datetime.now()).\
                    where((AssignmentStatus.enum_document_type_id == int(asInstance["enum_document_type_id"])) & 
                            (AssignmentStatus.entity_iin == asInstance["entity_iin"]) &
                            (AssignmentStatus.user_id == int(asInstance["user_id"])))

    result = await database.execute(query)
    
    query = insert(AssignmentStatus).values(
                is_active = asInstance["is_active"], 
                status = asInstance["status"],
                document_id = int(asInstance["document_id"]),
                date = datetime.now(),
                comment = asInstance["comment"],
                enum_document_type_id = int(asInstance["enum_document_type_id"]),
                entity_iin = asInstance["entity_iin"],
                user_id = int(asInstance["user_id"]))

    result = await database.execute(query)

    approval_processes = await is_approval_process_finished(parameters = asInstance)
    for key in approval_processes:
        if (approval_processes[key]['rejected']!=True and approval_processes[key]['approved']!=True):
            asyncio.create_task(check_approval_process(key))
    return {**asInstance, 'id': result}
    

async def update_assignment_status(asInstance: dict, assignment_status_id: int):

    query = update(AssignmentStatus).values(
                is_active = asInstance["is_active"], 
                status = asInstance["status"],
                document_id = int(asInstance["document_id"]),
                date = datetime.now(),
                comment = asInstance["comment"],
                enum_document_type_id = int(asInstance["enum_document_type_id"]),
                entity_iin = asInstance["entity_iin"],
                user_id = int(asInstance["user_id"])).\
                    where(AssignmentStatus.id == assignment_status_id)

    result = await database.execute(query)
    return asInstance
