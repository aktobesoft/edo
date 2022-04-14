from fastapi import APIRouter, Depends
from common_module.urls_module import common_parameters, query_params
from typing import List, Union

from documents.purchase_requisition.models import PurchaseRequisitionIn, PurchaseRequisitionNestedOut, PurchaseRequisitionOut, PurchaseRequisition
from documents.purchase_requisition import views


purchase_requisitionRouter = APIRouter()

@purchase_requisitionRouter.get('/', response_model = Union[List[PurchaseRequisitionNestedOut], List[PurchaseRequisitionOut]])
async def get_purchase_requisition_list(commons: dict = Depends(common_parameters)):
    records = await views.get_purchase_requisition_list(**commons)
    return records

@purchase_requisitionRouter.get('/{purchase_requisition_id}',response_model = Union[PurchaseRequisitionNestedOut, PurchaseRequisitionOut])
async def get_purchase_requisition_by_id(purchase_requisition_id : int, query_params: dict = Depends(query_params)):
    result = await views.get_purchase_requisition_by_id(purchase_requisition_id, **query_params)
    return result

@purchase_requisitionRouter.post('/', response_model = PurchaseRequisitionOut)
async def post_purchase_requisition(purchase_requisitionInstance : PurchaseRequisitionIn):
    purchase_requisitionDict = purchase_requisitionInstance.dict()
    result = await views.post_purchase_requisition(purchase_requisitionDict)
    return result

@purchase_requisitionRouter.put('/', response_model = PurchaseRequisitionOut)
async def update_purchase_requisition(newPurchaseRequisitionIn : PurchaseRequisitionOut):
    newPurchaseRequisitionIn = dict(newPurchaseRequisitionIn)
    result = await views.update_purchase_requisition(newPurchaseRequisitionIn)
    return newPurchaseRequisitionIn

@purchase_requisitionRouter.delete('/{purchase_requisition_id}')
async def delete_purchase_requisition_by_id(purchase_requisition_id : int):
    result = await views.delete_purchase_requisition_by_id(purchase_requisition_id)
    return result