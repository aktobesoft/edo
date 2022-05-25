from sqlalchemy import bindparam, func, select, insert, update, delete
from datetime import datetime, timezone

from core.db import database
from common_module.urls_module import correct_datetime

from catalogs.approval_status.models import ApprovalStatus
from catalogs.employee.models import Employee, employee_fillDataFromDict

async def get_approval_status_by_id(approval_status_id: int):
    query = select(ApprovalStatus).where(ApprovalStatus.id == approval_status_id)
    result = await database.fetch_one(query)
    return result

async def get_approval_status_nested_by_id(aproval_status_id: int):
    query = select(ApprovalStatus,
            Employee.id.label('employee_id'),
            Employee.email.label('employee_email'),
            Employee.name.label('employee_name')).\
            join(Employee, ApprovalStatus.employee_id == Employee.id, isouter=True).\
            where(ApprovalStatus.id == aproval_status_id)
    records = await database.fetch_one(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['employee'] = employee_fillDataFromDict(recordDict)
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
                    where((ApprovalStatus.document_type_id == int(asInstance["document_type_id"])) & 
                            (ApprovalStatus.approval_route_id == int(asInstance["approval_route_id"])) &
                            (ApprovalStatus.entity_iin == asInstance["entity_iin"]) &
                            (ApprovalStatus.employee_id == int(asInstance["employee_id"])))

    result = await database.execute(query)
    
    query = insert(ApprovalStatus).values(
                is_active = asInstance["is_active"], 
                status = asInstance["status"],
                document_id = int(asInstance["document_id"]),
                date = datetime.now(),
                comment = asInstance["comment"],
                document_type_id = int(asInstance["document_type_id"]),
                approval_route_id = int(asInstance["approval_route_id"]),
                entity_iin = asInstance["entity_iin"],
                employee_id = int(asInstance["employee_id"]))

    result = await database.execute(query)
    return {**asInstance, 'id': result}


async def update_approval_status(asInstance: dict, approval_status_id: int):

    query = update(ApprovalStatus).values(
                is_active = asInstance["is_active"], 
                status = asInstance["status"],
                document_id = int(asInstance["document_id"]),
                date = datetime.now(),
                comment = asInstance["comment"],
                document_type_id = int(asInstance["document_type_id"]),
                approval_route_id = int(asInstance["approval_route_id"]),
                entity_iin = asInstance["entity_iin"],
                employee_id = int(asInstance["employee_id"])).\
                    where(ApprovalStatus.id == approval_status_id)

    result = await database.execute(query)
    return asInstance
