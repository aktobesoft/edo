from sqlalchemy import select, insert, update, delete
from core.db import database
import asyncpg
from datetime import date, datetime, timezone
from common_module.urls_module import correct_datetime, correct_datetime

from documents.purchase_requisition.models import PurchaseRequisition, PurchaseRequisitionIn, PurchaseRequisitionOut
from references.business_type.models import BusinessType
from references.counterparty.models import Counterparty, counterparty_fillDataFromDict
from references.document_type.models import DocumentType, document_type_fillDataFromDict
from references.entity.models import Entity, entity_fillDataFromDict
from references.user.models import User


async def get_purchase_requisition_by_id(purchase_requisition_id: int, **kwargs):
    if(kwargs['nested']):
        return await get_purchase_requisition_nested_by_id(purchase_requisition_id, **kwargs)
    queryPurchaseRequisition = select(PurchaseRequisition).where(PurchaseRequisition.id == purchase_requisition_id)
    resultPurchaseRequisition = await database.fetch_one(queryPurchaseRequisition)
    return resultPurchaseRequisition

async def get_purchase_requisition_nested_by_id(purchase_requisition_id: int, **kwargs):
    queryPurchaseRequisition = select(
                PurchaseRequisition,
                Entity.name.label("entity_name"),
                Entity.iin.label("entity_iin"),
                Counterparty.iin.label("counterparty_iin"), 
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
    return recordDict

async def delete_purchase_requisition_by_id(purchase_requisition_id: int):
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
                PurchaseRequisition.entity_iin).order_by(
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
                Entity.iin.label("entity_iin"),
                Counterparty.iin.label("counterparty_iin"), 
                Counterparty.name.label("counterparty_name"),
                DocumentType.name.label("document_type_name"),
                DocumentType.description.label("document_type_description")).\
                    join(
                Entity, PurchaseRequisition.entity_iin == Entity.iin, isouter=True).\
                    join(
                Counterparty, PurchaseRequisition.counterparty_iin == Counterparty.iin, isouter=True).\
                    join(
                DocumentType, PurchaseRequisition.document_type_id == DocumentType.id, isouter=True).\
                    order_by(
                PurchaseRequisition.id).\
                    limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['entity'] = entity_fillDataFromDict(recordDict)
        recordDict['document_type'] = document_type_fillDataFromDict(recordDict)
        recordDict['counterparty'] = counterparty_fillDataFromDict(recordDict)
        listValue.append(recordDict)
    return listValue

async def post_purchase_requisition(purchaseRequisitionInstance : dict):

    purchaseRequisitionInstance["date"] = correct_datetime(purchaseRequisitionInstance["date"])
    
    query = insert(PurchaseRequisition).values(
                guid = purchaseRequisitionInstance["guid"], 
                number = purchaseRequisitionInstance["number"], 
                date = purchaseRequisitionInstance["date"],
                comment = purchaseRequisitionInstance["comment"], 
                sum = float(purchaseRequisitionInstance["sum"]), 
                counterparty_iin = purchaseRequisitionInstance["counterparty_iin"], 
                document_type_id = int(purchaseRequisitionInstance["document_type_id"]), 
                entity_iin = purchaseRequisitionInstance["entity_iin"])
    newPurchaseRequisitionId = await database.execute(query)

    return {**purchaseRequisitionInstance, 'id': newPurchaseRequisitionId}

async def update_purchase_requisition(purchaseRequisitionInstance: dict):

    purchaseRequisitionInstance["date"] = correct_datetime(purchaseRequisitionInstance["date"])

    query = update(PurchaseRequisition).values(
                number = purchaseRequisitionInstance["number"], 
                date = purchaseRequisitionInstance["date"],
                comment = purchaseRequisitionInstance["comment"], 
                sum = purchaseRequisitionInstance["sum"], 
                counterparty_iin = purchaseRequisitionInstance["counterparty_iin"], 
                document_type_id = purchaseRequisitionInstance["document_type_id"], 
                guid = purchaseRequisitionInstance["guid"], 
                entity_iin = purchaseRequisitionInstance["entity_iin"]).where(
                    PurchaseRequisition.id == purchaseRequisitionInstance['id'])

    result = await database.execute(query)
    return purchaseRequisitionInstance

