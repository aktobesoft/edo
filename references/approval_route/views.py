from sqlalchemy import select, insert, update, delete
import asyncpg
from core.db import database
from common_module.urls_module import correct_datetime

from references.approval_route.models import ApprovalRoute, ApprovalRouteIn

async def get_approval_route_by_id(approval_route_id: int):
    query = select(ApprovalRoute).where(ApprovalRoute.id == approval_route_id)
    result = await database.fetch_one(query)
    return result

async def get_approval_route_nested_by_id(approval_route_id: int):
    query = select(ApprovalRoute).where(ApprovalRoute.id == approval_route_id)
    result = await database.fetch_one(query)
    return result

async def delete_approval_route_by_id(approval_route_id: int):
    query = delete(ApprovalRoute).where(ApprovalRoute.id == approval_route_id)
    result = await database.execute(query)
    return result

async def get_approval_route_list(limit: int = 100,skip: int = 0,**kwargs):

    query = select(ApprovalRoute).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def post_approval_route(arInstance : dict):
    
    query = insert(ApprovalRoute).values(
                is_active = arInstance["is_active"], 
                level = int(arInstance["level"]),
                type = arInstance["type"],
                document_id = int(arInstance["document_id"]),
                entity_iin = arInstance["entity_iin"],
                employee_id = int(arInstance["employee_id"]),
                approval_template_id = int(arInstance["approval_template_id"]),
                approval_process_id = int(arInstance["approval_process_id"]))
    result = await database.execute(query)
    return {**arInstance, 'id': result}

async def update_approval_route(arInstance: dict):

    query = update(ApprovalRoute).values(
                 is_active = arInstance["is_active"], 
                level = int(arInstance["level"]),
                type = arInstance["type"],
                document_id = int(arInstance["document_id"]),
                entity_iin = arInstance["entity_iin"],
                employee_id = int(arInstance["employee_id"]),
                approval_template_id = int(arInstance["approval_template_id"]),
                approval_process_id = int(arInstance["approval_process_id"])).\
                    where(ApprovalRoute.id == int(arInstance['id']))

    result = await database.execute(query)
    return arInstance