from certifi import where
from fastapi import HTTPException
from sqlalchemy import String, func, null, select, insert, tuple_, update, delete
from catalogs.approval_route.models import ApprovalRoute
from catalogs.approval_route.views import get_approval_routes_by_metadata
from catalogs.approval_status.models import ApprovalStatus
from catalogs.enum_types.views import enum_document_type_fill_data_from_dict, get_enum_document_type_id_by_metadata_name
from catalogs.user.models import User, fill_user_data_from_dict
from core.db import database
from common_module.urls_module import correct_datetime, correct_datetime, is_need_filter, is_key_exist

from documents.purchase_requisition.models import PurchaseRequisition, PurchaseRequisitionOut
from documents.purchase_requisition_items.views import delete_all_pr_items_by_purchase_requisition, get_pr_items_list_by_purchase_requisition_id, post_pr_items_by_purchase_requisition, update_pr_items_by_purchase_requisition
from catalogs.approval_process.models import ApprovalProcess
from catalogs.counterparty.models import Counterparty, counterparty_fill_data_from_dict
from catalogs.enum_types.models import EnumDocumentType
from catalogs.entity.models import Entity, entity_fill_data_from_dict


async def get_purchase_requisition_by_id(purchase_requisition_id: int, **kwargs):
    if(kwargs['nested']):
        return await get_purchase_requisition_nested_by_id(purchase_requisition_id, **kwargs)
    
    purchase_requisition_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("purchase_requisition")
    query = select(PurchaseRequisition).where(PurchaseRequisition.id == purchase_requisition_id).\
            where(PurchaseRequisition.enum_document_type_id == purchase_requisition_enum_document_type_id)
    
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(PurchaseRequisition.entity_iin.in_(kwargs['entity_iin_list']))

    result = await database.fetch_one(query)
    if result == None:
        raise HTTPException(status_code=404, detail="Item not found") 
    resultPurchaseRequisition = dict(result)
    resultPurchaseRequisition['items'] = await get_pr_items_list_by_purchase_requisition_id(purchase_requisition_id)
    return resultPurchaseRequisition

async def get_purchase_requisition_count(**kwargs):
    purchase_requisition_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("purchase_requisition")
    query = select(func.count(PurchaseRequisition.id)).where(PurchaseRequisition.enum_document_type_id == purchase_requisition_enum_document_type_id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(PurchaseRequisition.entity_iin.in_(kwargs['entity_iin_list']))
    return await database.execute(query)

async def get_purchase_requisition_nested_by_id(purchase_requisition_id: int, **kwargs):
    purchase_requisition_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("purchase_requisition")
    query = select(
                PurchaseRequisition,
                Entity.name.label("entity_name"),
                Entity.iin.label("entity_iin"),
                Entity.id.label("entity_id"),
                User.id.label("user_id"),
                User.name.label("user_name"),
                User.email.label("user_email"),
                Counterparty.iin.label("counterparty_iin"), 
                Counterparty.id.label("counterparty_id"),
                Counterparty.name.label("counterparty_name"),
                EnumDocumentType.name.label("enum_document_type_name"),
                ApprovalProcess.status.label("status"),
                ApprovalProcess.id.label("approval_process_id"),
                ApprovalProcess.start_date.label("approval_process_start_date"),
                ApprovalProcess.end_date.label("approval_process_end_date"),
                EnumDocumentType.description.label("enum_document_type_description")).\
                join(ApprovalProcess, (PurchaseRequisition.id == ApprovalProcess.document_id) & 
                    (PurchaseRequisition.enum_document_type_id == ApprovalProcess.enum_document_type_id) & (ApprovalProcess.is_active), isouter=True).\
                join(User, PurchaseRequisition.author_id == User.id, isouter=True).\
                join(Entity, PurchaseRequisition.entity_iin == Entity.iin, isouter=True).\
                join(Counterparty, PurchaseRequisition.counterparty_iin == Counterparty.iin, isouter=True).\
                join(EnumDocumentType, PurchaseRequisition.enum_document_type_id == EnumDocumentType.id, isouter=True).\
                where(PurchaseRequisition.id == purchase_requisition_id).\
                where(PurchaseRequisition.enum_document_type_id == purchase_requisition_enum_document_type_id)       
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(PurchaseRequisition.entity_iin.in_(kwargs['entity_iin_list']))
    result = await database.fetch_one(query)

    if result == None:
        raise HTTPException(status_code=404, detail="Item not found") 

    recordDict = dict(result)
    recordDict['entity'] = entity_fill_data_from_dict(recordDict)
    recordDict['enum_document_type'] = enum_document_type_fill_data_from_dict(recordDict)
    recordDict['counterparty'] = counterparty_fill_data_from_dict(recordDict)
    recordDict['author'] = fill_user_data_from_dict(recordDict)
    recordDict['items'] = await get_pr_items_list_by_purchase_requisition_id(purchase_requisition_id)

    if(is_key_exist('include_approve_route', kwargs)):
        kwargs['approval_process_id'] = [recordDict['approval_process_id']]
        routes_result  = await get_approval_routes_by_metadata('purchase_requisition', **kwargs)
        include_approve_route = True
    else:
        include_approve_route = False
    
    if(include_approve_route):
            if recordDict['approval_process_id'] in routes_result:
                recordDict['current_approval_routes'] = routes_result[recordDict['approval_process_id']]['current_approval_routes']
                recordDict['all_approval_routes'] = routes_result[recordDict['approval_process_id']]['all_approval_routes']
            else:
                recordDict['current_approval_routes'] = []
                recordDict['all_approval_routes'] = []

    return recordDict

async def delete_purchase_requisition_by_id(purchase_requisition_id: int, **kwargs):
    await delete_all_pr_items_by_purchase_requisition(purchase_requisition_id)
    query = delete(PurchaseRequisition).where(PurchaseRequisition.id == purchase_requisition_id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(PurchaseRequisition.entity_iin.in_(kwargs['entity_iin_list']))
    resultPurchaseRequisition = await database.execute(query)

    return resultPurchaseRequisition

async def get_purchase_requisition_list(limit: int = 100, skip: int = 0, **kwargs)->list[PurchaseRequisitionOut]:
    purchase_requisition_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("purchase_requisition")
    if(kwargs['nested']):
        return await get_purchase_requisition_nested_list(limit, skip, **kwargs)

    query = select( 
                PurchaseRequisition.id, 
                PurchaseRequisition.guid, 
                PurchaseRequisition.number, 
                PurchaseRequisition.date, 
                PurchaseRequisition.comment, 
                PurchaseRequisition.sum, 
                PurchaseRequisition.counterparty_iin, 
                PurchaseRequisition.enum_document_type_id, 
                PurchaseRequisition.entity_iin,
                PurchaseRequisition.author_id,
                ApprovalProcess.status,
                ApprovalProcess.id.label("approval_process_id"),
                ApprovalProcess.start_date.label("approval_process_start_date"),
                ApprovalProcess.end_date.label("approval_process_end_date")).\
                join(ApprovalProcess, (PurchaseRequisition.id == ApprovalProcess.document_id) & 
                    (PurchaseRequisition.enum_document_type_id == ApprovalProcess.enum_document_type_id) & (ApprovalProcess.is_active), isouter=True).\
                where(PurchaseRequisition.enum_document_type_id == purchase_requisition_enum_document_type_id).\
                order_by(PurchaseRequisition.id).limit(limit).offset(skip)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(PurchaseRequisition.entity_iin.in_(kwargs['entity_iin_list']))

    if(is_key_exist('include_approve_route', kwargs)):
        include_approve_route = True
        routes_result  = await get_approval_routes_by_metadata('purchase_requisition', **kwargs)
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

async def get_purchase_requisition_nested_list(limit: int = 100, skip: int = 0, **kwargs)->list[PurchaseRequisitionOut]:
    purchase_requisition_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("purchase_requisition")
    query = select( 
                PurchaseRequisition.id, 
                PurchaseRequisition.guid, 
                PurchaseRequisition.number, 
                PurchaseRequisition.date, 
                PurchaseRequisition.comment, 
                PurchaseRequisition.sum, 
                PurchaseRequisition.counterparty_iin.label('counterparty_iin'), 
                PurchaseRequisition.enum_document_type_id.label('enum_document_type_id'), 
                PurchaseRequisition.entity_iin.label('entity_iin'),
                Entity.name.label("entity_name"),
                Entity.id.label("entity_id"),
                User.id.label("user_id"),
                User.name.label("user_name"),
                User.email.label("user_email"),
                Counterparty.id.label("counterparty_id"), 
                Counterparty.name.label("counterparty_name"),
                EnumDocumentType.name.label("enum_document_type_name"),
                EnumDocumentType.description.label("enum_document_type_description"),
                ApprovalProcess.status,
                ApprovalProcess.id.label("approval_process_id"),
                ApprovalProcess.start_date.label("approval_process_start_date"),
                ApprovalProcess.end_date.label("approval_process_end_date")).\
                join(Entity, PurchaseRequisition.entity_iin == Entity.iin, isouter=True).\
                join(User, PurchaseRequisition.author_id == User.id, isouter=True).\
                join(Counterparty, PurchaseRequisition.counterparty_iin == Counterparty.iin, isouter=True).\
                join(EnumDocumentType, PurchaseRequisition.enum_document_type_id == EnumDocumentType.id, isouter=True).\
                join(ApprovalProcess, (PurchaseRequisition.id == ApprovalProcess.document_id) & 
                    (PurchaseRequisition.enum_document_type_id == ApprovalProcess.enum_document_type_id) & (ApprovalProcess.is_active), isouter=True).\
                where(PurchaseRequisition.enum_document_type_id == purchase_requisition_enum_document_type_id).\
                    order_by(PurchaseRequisition.id)
               
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(PurchaseRequisition.entity_iin.in_(kwargs['entity_iin_list']))

    records = await database.fetch_all(query)
    listValue = []
    
    if (len(records) == 0):
        return listValue
    
    if(is_key_exist('include_approve_route', kwargs)):
        include_approve_route = True
        routes_result  = await get_approval_routes_by_metadata('purchase_requisition', **kwargs)
    else:
        include_approve_route = False

    for rec in records:
        recordDict = dict(rec)
        recordDict['entity'] = entity_fill_data_from_dict(rec)
        recordDict['enum_document_type'] = enum_document_type_fill_data_from_dict(rec)
        recordDict['counterparty'] = counterparty_fill_data_from_dict(rec)
        recordDict['author'] = fill_user_data_from_dict(rec)
        if(include_approve_route):
            if recordDict['approval_process_id'] in routes_result:
                recordDict['current_approval_routes'] = routes_result[recordDict['approval_process_id']]['current_approval_routes']
                recordDict['all_approval_routes'] = routes_result[recordDict['approval_process_id']]['all_approval_routes']
            else:
                recordDict['current_approval_routes'] = []
                recordDict['all_approval_routes'] = []
        listValue.append(recordDict)
    return listValue


    
async def get_max_purchase_requisition_number(entity_iin: str)->str:
    query = select(func.max(PurchaseRequisition.number).label('number')).where(PurchaseRequisition.entity_iin == entity_iin)
    result = await database.fetch_one(query)
    
    if result == None or result['number'] == null or result['number'] == None:
        number = 1
    else:
        number = result['number']
        number = number + 1

    return number

async def post_purchase_requisition(purchaseRequisitionInstance : dict, **kwargs):
    # RLS
    if(is_need_filter('entity_iin_list', kwargs) and purchaseRequisitionInstance["entity_iin"] not in kwargs['entity_iin_list']):
        raise HTTPException(status_code=403, detail="Forbidden")

    purchase_requisition_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("purchase_requisition")

    purchaseRequisitionInstance["date"] = correct_datetime(purchaseRequisitionInstance["date"])
    max_number = await get_max_purchase_requisition_number(purchaseRequisitionInstance["entity_iin"])
    query = insert(PurchaseRequisition).values(
                guid = purchaseRequisitionInstance["guid"], 
                number = max_number, 
                date = purchaseRequisitionInstance["date"],
                comment = purchaseRequisitionInstance["comment"], 
                sum = float(purchaseRequisitionInstance["sum"]), 
                counterparty_iin = purchaseRequisitionInstance["counterparty_iin"], 
                enum_document_type_id = purchase_requisition_enum_document_type_id, 
                author_id = kwargs['current_user']['id'],
                entity_iin = purchaseRequisitionInstance["entity_iin"])

    newPurchaseRequisitionId = await database.execute(query)
    await post_pr_items_by_purchase_requisition(purchaseRequisitionInstance["items"], newPurchaseRequisitionId)
    return {**purchaseRequisitionInstance, 'id': newPurchaseRequisitionId}

async def update_purchase_requisition(purchaseRequisitionInstance: dict, purchaseRequisitionId: int, **kwargs):
    purchaseRequisitionInstance["date"] = correct_datetime(purchaseRequisitionInstance["date"])
    purchase_requisition_enum_document_type_id = await get_enum_document_type_id_by_metadata_name("purchase_requisition")

    query = update(PurchaseRequisition).values(
                date = purchaseRequisitionInstance["date"],
                comment = purchaseRequisitionInstance["comment"], 
                sum = purchaseRequisitionInstance["sum"], 
                counterparty_iin = purchaseRequisitionInstance["counterparty_iin"], 
                enum_document_type_id = purchase_requisition_enum_document_type_id, 
                author_id = kwargs['current_user']['id'],
                guid = purchaseRequisitionInstance["guid"]).where(
                    (PurchaseRequisition.id == purchaseRequisitionId) & 
                    (PurchaseRequisition.entity_iin == purchaseRequisitionInstance["entity_iin"]))
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(PurchaseRequisition.entity_iin.in_(kwargs['entity_iin_list']))

    result = await database.execute(query)
    await update_pr_items_by_purchase_requisition(purchaseRequisitionInstance["items"], purchaseRequisitionId)
    return purchaseRequisitionInstance

