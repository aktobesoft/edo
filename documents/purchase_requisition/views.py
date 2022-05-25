from sqlalchemy import func, null, select, insert, update, delete
from core.db import database
from common_module.urls_module import correct_datetime, correct_datetime

from documents.purchase_requisition.models import PurchaseRequisition, PurchaseRequisitionOut
from documents.purchase_requisition_items.views import delete_all_pr_items_by_purchase_requisition, get_pr_items_list_by_purchase_requisition_id, post_pr_items_by_purchase_requisition, update_pr_items_by_purchase_requisition
from catalogs.approval_process.models import ApprovalProcess
from catalogs.counterparty.models import Counterparty, counterparty_fillDataFromDict
from catalogs.document_type.models import DocumentType, document_type_fillDataFromDict
from catalogs.entity.models import Entity, entity_fillDataFromDict


async def get_purchase_requisition_by_id(purchase_requisition_id: int, **kwargs):
    if(kwargs['nested']):
        return await get_purchase_requisition_nested_by_id(purchase_requisition_id, **kwargs)
    queryPurchaseRequisition = select(PurchaseRequisition).where(PurchaseRequisition.id == purchase_requisition_id)
    result = await database.fetch_one(queryPurchaseRequisition)
    resultPurchaseRequisition = dict(result)
    resultPurchaseRequisition['items'] = await get_pr_items_list_by_purchase_requisition_id(purchase_requisition_id, **kwargs)
    return resultPurchaseRequisition

async def get_purchase_requisition_count():
    query = select(func.count(PurchaseRequisition.id))
    return await database.execute(query)

async def get_purchase_requisition_nested_by_id(purchase_requisition_id: int, **kwargs):
    queryPurchaseRequisition = select(
                PurchaseRequisition,
                Entity.name.label("entity_name"),
                Entity.iin.label("entity_iin"),
                Entity.id.label("entity_id"),
                Counterparty.iin.label("counterparty_iin"), 
                Counterparty.id.label("counterparty_id"),
                Counterparty.name.label("counterparty_name"),
                DocumentType.name.label("document_type_name"),
                DocumentType.description.label("document_type_description")).\
                    join(Entity, PurchaseRequisition.entity_iin == Entity.iin, isouter=True).\
                    join(Counterparty, PurchaseRequisition.counterparty_iin == Counterparty.iin, isouter=True).\
                    join(DocumentType, PurchaseRequisition.document_type_id == DocumentType.id, isouter=True).\
                    where(PurchaseRequisition.id == purchase_requisition_id)

    resultPurchaseRequisition = await database.fetch_one(queryPurchaseRequisition)
    recordDict = dict(resultPurchaseRequisition)
    recordDict['entity'] = entity_fillDataFromDict(resultPurchaseRequisition)
    recordDict['document_type'] = document_type_fillDataFromDict(resultPurchaseRequisition)
    recordDict['counterparty'] = counterparty_fillDataFromDict(resultPurchaseRequisition)
    recordDict['items'] = await get_pr_items_list_by_purchase_requisition_id(purchase_requisition_id, **kwargs)
    return recordDict

async def delete_purchase_requisition_by_id(purchase_requisition_id: int):
    await delete_all_pr_items_by_purchase_requisition(purchase_requisition_id)
    queryPurchaseRequisition = delete(PurchaseRequisition).where(PurchaseRequisition.id == purchase_requisition_id)
    resultPurchaseRequisition = await database.execute(queryPurchaseRequisition)

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
                ApprovalProcess.status).\
                    join(
                ApprovalProcess, (PurchaseRequisition.id == ApprovalProcess.document_id) & 
                    (PurchaseRequisition.document_type_id == ApprovalProcess.document_type_id) & (ApprovalProcess.is_active), isouter=True).\
                    order_by(
                PurchaseRequisition.id).limit(limit).offset(skip)
   
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
                ApprovalProcess.status).\
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
                PurchaseRequisition.id).\
                    limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['entity'] = entity_fillDataFromDict(rec)
        recordDict['document_type'] = document_type_fillDataFromDict(rec)
        recordDict['counterparty'] = counterparty_fillDataFromDict(rec)
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

async def post_purchase_requisition(purchaseRequisitionInstance : dict):

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

async def update_purchase_requisition(purchaseRequisitionInstance: dict, purchaseRequisitionId: int):

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

    result = await database.execute(query)
    await update_pr_items_by_purchase_requisition(purchaseRequisitionInstance["items"], purchaseRequisitionId)
    return purchaseRequisitionInstance

