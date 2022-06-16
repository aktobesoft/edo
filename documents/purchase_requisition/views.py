from certifi import where
from fastapi import HTTPException
from sqlalchemy import String, func, null, select, insert, tuple_, update, delete
from catalogs.approval_route.models import ApprovalRoute
from catalogs.approval_status.models import ApprovalStatus
from catalogs.document_type.views import get_document_type_id_by_metadata_name
from core.db import database
from common_module.urls_module import correct_datetime, correct_datetime, is_need_filter

from documents.purchase_requisition.models import PurchaseRequisition, PurchaseRequisitionOut
from documents.purchase_requisition_items.views import delete_all_pr_items_by_purchase_requisition, get_pr_items_list_by_purchase_requisition_id, post_pr_items_by_purchase_requisition, update_pr_items_by_purchase_requisition
from catalogs.approval_process.models import ApprovalProcess
from catalogs.counterparty.models import Counterparty, counterparty_fillDataFromDict
from catalogs.document_type.models import DocumentType, document_type_fillDataFromDict
from catalogs.entity.models import Entity, entity_fillDataFromDict


async def get_purchase_requisition_by_id(purchase_requisition_id: int, **kwargs):
    if(kwargs['nested']):
        return await get_purchase_requisition_nested_by_id(purchase_requisition_id, **kwargs)
    query = select(PurchaseRequisition).where(PurchaseRequisition.id == purchase_requisition_id)
    
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(PurchaseRequisition.entity_iin.in_(kwargs['entity_iin_list']))

    result = await database.fetch_one(query)
    if result == None:
        raise HTTPException(status_code=404, detail="Item not found") 
    resultPurchaseRequisition = dict(result)
    resultPurchaseRequisition['items'] = await get_pr_items_list_by_purchase_requisition_id(purchase_requisition_id, **kwargs)
    return resultPurchaseRequisition

async def get_purchase_requisition_count(**kwargs):
    query = select(func.count(PurchaseRequisition.id))
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(PurchaseRequisition.entity_iin.in_(kwargs['entity_iin_list']))
    return await database.execute(query)

async def get_purchase_requisition_nested_by_id(purchase_requisition_id: int, **kwargs):
    query = select(
                PurchaseRequisition,
                Entity.name.label("entity_name"),
                Entity.iin.label("entity_iin"),
                Entity.id.label("entity_id"),
                Counterparty.iin.label("counterparty_iin"), 
                Counterparty.id.label("counterparty_id"),
                Counterparty.name.label("counterparty_name"),
                DocumentType.name.label("document_type_name"),
                ApprovalProcess.status.label("status"),
                DocumentType.description.label("document_type_description")).\
                    join(ApprovalProcess, (PurchaseRequisition.id == ApprovalProcess.document_id) & 
                        (PurchaseRequisition.document_type_id == ApprovalProcess.document_type_id) & (ApprovalProcess.is_active), isouter=True).\
                    join(Entity, PurchaseRequisition.entity_iin == Entity.iin, isouter=True).\
                    join(Counterparty, PurchaseRequisition.counterparty_iin == Counterparty.iin, isouter=True).\
                    join(DocumentType, PurchaseRequisition.document_type_id == DocumentType.id, isouter=True).\
                    where(PurchaseRequisition.id == purchase_requisition_id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(PurchaseRequisition.entity_iin.in_(kwargs['entity_iin_list']))
    resultPurchaseRequisition = await database.fetch_one(query)
    recordDict = dict(resultPurchaseRequisition)
    recordDict['entity'] = entity_fillDataFromDict(resultPurchaseRequisition)
    recordDict['document_type'] = document_type_fillDataFromDict(resultPurchaseRequisition)
    recordDict['counterparty'] = counterparty_fillDataFromDict(resultPurchaseRequisition)
    recordDict['items'] = await get_pr_items_list_by_purchase_requisition_id(purchase_requisition_id, **kwargs)
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
                PurchaseRequisition.document_type_id, 
                PurchaseRequisition.entity_iin,
                ApprovalProcess.status,
                ApprovalProcess.id.label("process_id")).\
                    join(
                ApprovalProcess, (PurchaseRequisition.id == ApprovalProcess.document_id) & 
                    (PurchaseRequisition.document_type_id == ApprovalProcess.document_type_id) & (ApprovalProcess.is_active), isouter=True).\
                    order_by(
                PurchaseRequisition.id).limit(limit).offset(skip)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(PurchaseRequisition.entity_iin.in_(kwargs['entity_iin_list']))

    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def get_purchase_requisition_nested_list(limit: int = 100, skip: int = 0, **kwargs)->list[PurchaseRequisitionOut]:
    query = select( 
                PurchaseRequisition.id, 
                PurchaseRequisition.guid, 
                PurchaseRequisition.number, 
                PurchaseRequisition.date, 
                PurchaseRequisition.comment, 
                PurchaseRequisition.sum, 
                PurchaseRequisition.counterparty_iin.label('counterparty_iin'), 
                PurchaseRequisition.document_type_id.label('document_type_id'), 
                PurchaseRequisition.entity_iin.label('entity_iin'),
                Entity.name.label("entity_name"),
                Entity.id.label("entity_id"),
                Counterparty.id.label("counterparty_id"), 
                Counterparty.name.label("counterparty_name"),
                DocumentType.name.label("document_type_name"),
                DocumentType.description.label("document_type_description"),
                ApprovalProcess.status,
                ApprovalProcess.id.label("process_id")).\
                    join(
                Entity, PurchaseRequisition.entity_iin == Entity.iin, isouter=True).\
                    join(
                Counterparty, PurchaseRequisition.counterparty_iin == Counterparty.iin, isouter=True).\
                    join(
                DocumentType, PurchaseRequisition.document_type_id == DocumentType.id, isouter=True).\
                    join(
                ApprovalProcess, (PurchaseRequisition.id == ApprovalProcess.document_id) & 
                    (PurchaseRequisition.document_type_id == ApprovalProcess.document_type_id) & (ApprovalProcess.is_active), isouter=True).\
                    order_by(
                PurchaseRequisition.id)
    print(limit, skip)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(PurchaseRequisition.entity_iin.in_(kwargs['entity_iin_list']))

    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['entity'] = entity_fillDataFromDict(rec)
        recordDict['document_type'] = document_type_fillDataFromDict(rec)
        recordDict['counterparty'] = counterparty_fillDataFromDict(rec)
        listValue.append(recordDict)
    return listValue

async def get_purchase_requisition_nested_list_with_routs(**kwargs):
    purchase_requisition_document_type_id = await get_document_type_id_by_metadata_name("purchase_requisition")
    query_min = select(func.min(ApprovalRoute.level).label("min_level"),
                        ApprovalProcess.id.label("approval_process_id")).\
                    join(ApprovalRoute, (ApprovalProcess.id == ApprovalRoute.approval_process_id), isouter=True).\
                    join(ApprovalStatus, (ApprovalRoute.id == ApprovalStatus.approval_route_id) & (ApprovalRoute.is_active) & (ApprovalStatus.status == None), isouter=True).\
                    where(ApprovalProcess.is_active).\
                    group_by(ApprovalProcess.id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query_min = query_min.where(ApprovalProcess.entity_iin.in_(kwargs['entity_iin_list']))

    query_current_approval_route = select(
            func.lower("current_approval_route", type_=String).label('list_type'), 
            ApprovalRoute.employee_id,
            ApprovalRoute.level,
            ApprovalRoute.type,
            ApprovalProcess.id.label('approval_process_id'),
            ApprovalRoute.id.label('route_id'),
            ApprovalStatus.status.label('route_status'),
            ApprovalStatus.comment.label('route_comment'),
            ApprovalStatus.date.label('route_date')).\
            join(ApprovalRoute, (ApprovalProcess.id == ApprovalRoute.approval_process_id), isouter=True).\
            join(ApprovalStatus, (ApprovalRoute.id == ApprovalStatus.approval_route_id) & (ApprovalRoute.is_active) & (ApprovalStatus.status == None), isouter=True).\
            where(ApprovalProcess.is_active).\
            where(tuple_(ApprovalRoute.level, ApprovalRoute.approval_process_id).in_(query_min)).\
            order_by(ApprovalProcess.id, ApprovalRoute.level, ApprovalRoute.type)
    

    query_all_approval_route = select(
            func.lower("all_approval_route", type_=String).label('list_type'), 
            ApprovalRoute.employee_id,
            ApprovalRoute.level,
            ApprovalRoute.type,
            ApprovalProcess.id.label('approval_process_id'),
            ApprovalRoute.id.label('route_id'),
            ApprovalStatus.status.label('route_status'),
            ApprovalStatus.comment.label('route_comment'),
            ApprovalStatus.date.label('route_date')).\
            join(ApprovalRoute, (ApprovalProcess.id == ApprovalRoute.approval_process_id), isouter=True).\
            join(ApprovalStatus, (ApprovalRoute.id == ApprovalStatus.approval_route_id) & (ApprovalRoute.is_active) & (ApprovalStatus.status == None), isouter=True).\
            where(ApprovalProcess.is_active).\
            order_by(ApprovalProcess.id, ApprovalRoute.level, ApprovalRoute.type)
            # where(ApprovalRoute.approval_process_id).in_(kwargs['approval_process_id_list'])
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query_all_approval_route = query_all_approval_route.where(ApprovalProcess.entity_iin.in_(kwargs['entity_iin_list']))

    query = query_current_approval_route.union_all(query_all_approval_route).alias('approval_route_list')           
    
    print(query)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        # recordDict['entity'] = entity_fillDataFromDict(rec)
        # recordDict['document_type'] = document_type_fillDataFromDict(rec)
        # recordDict['counterparty'] = counterparty_fillDataFromDict(rec)
        listValue.append(recordDict)
    return listValue
    
async def get_max_purchase_requisition_number(entity_iin: str)->str:
    query = select(func.max(PurchaseRequisition.number).label('number')).where(PurchaseRequisition.entity_iin == entity_iin)
    result = await database.fetch_one(query)
    
    if result == None or result['number'] == null or result['number'] == None:
        number = 1
    else:
        number = ''.join(filter(str.isdigit, result['number']))
        number = int(number) + 1

    return str(number)

async def post_purchase_requisition(purchaseRequisitionInstance : dict, **kwargs):
    # RLS
    if(is_need_filter('entity_iin_list', kwargs) and purchaseRequisitionInstance["entity_iin"] not in kwargs['entity_iin_list']):
        raise HTTPException(status_code=403, detail="Forbidden")

    purchaseRequisitionInstance["date"] = correct_datetime(purchaseRequisitionInstance["date"])
    max_number = await get_max_purchase_requisition_number(purchaseRequisitionInstance["entity_iin"])
    query = insert(PurchaseRequisition).values(
                guid = purchaseRequisitionInstance["guid"], 
                number = max_number, 
                date = purchaseRequisitionInstance["date"],
                comment = purchaseRequisitionInstance["comment"], 
                sum = float(purchaseRequisitionInstance["sum"]), 
                counterparty_iin = purchaseRequisitionInstance["counterparty_iin"], 
                document_type_id = int(purchaseRequisitionInstance["document_type_id"]), 
                entity_iin = purchaseRequisitionInstance["entity_iin"])

    newPurchaseRequisitionId = await database.execute(query)
    await post_pr_items_by_purchase_requisition(purchaseRequisitionInstance["items"], newPurchaseRequisitionId)
    return {**purchaseRequisitionInstance, 'id': newPurchaseRequisitionId}

async def update_purchase_requisition(purchaseRequisitionInstance: dict, purchaseRequisitionId: int, **kwargs):

    purchaseRequisitionInstance["date"] = correct_datetime(purchaseRequisitionInstance["date"])

    query = update(PurchaseRequisition).values(
                number = purchaseRequisitionInstance["number"], 
                date = purchaseRequisitionInstance["date"],
                comment = purchaseRequisitionInstance["comment"], 
                sum = purchaseRequisitionInstance["sum"], 
                counterparty_iin = purchaseRequisitionInstance["counterparty_iin"], 
                document_type_id = int(purchaseRequisitionInstance["document_type_id"]), 
                guid = purchaseRequisitionInstance["guid"]).where(
                    (PurchaseRequisition.id == purchaseRequisitionId) & 
                    (PurchaseRequisition.entity_iin == purchaseRequisitionInstance["entity_iin"])
                    )
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query = query.where(PurchaseRequisition.entity_iin.in_(kwargs['entity_iin_list']))

    result = await database.execute(query)
    await update_pr_items_by_purchase_requisition(purchaseRequisitionInstance["items"], purchaseRequisitionId)
    return purchaseRequisitionInstance

