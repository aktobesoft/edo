from fastapi import APIRouter, Depends
from common_module.urls_module import qp_select_list, qp_select_one, qp_update, qp_insert
from typing import List, Union

from documents.purchase_requisition.models import PurchaseRequisitionIn, PurchaseRequisitionNestedOut, PurchaseRequisitionOut, PurchaseRequisition
from documents.purchase_requisition import views


purchase_requisitionRouter = APIRouter()

@purchase_requisitionRouter.get('/', response_model = Union[List[PurchaseRequisitionNestedOut], List[PurchaseRequisitionOut]])
async def get_purchase_requisition_list(commons: dict = Depends(qp_select_list)):
    records = await views.get_purchase_requisition_list(**commons)
    return records

@purchase_requisitionRouter.get('/{purchase_requisition_id}',response_model = Union[PurchaseRequisitionNestedOut, PurchaseRequisitionOut])
async def get_purchase_requisition_by_id(purchase_requisition_id : int, qp_select_one: dict = Depends(qp_select_one)):
    result = await views.get_purchase_requisition_by_id(purchase_requisition_id, **qp_select_one)
    return result

@purchase_requisitionRouter.post('/', response_model = Union[PurchaseRequisitionNestedOut,PurchaseRequisitionOut])
async def post_purchase_requisition(purchase_requisitionInstance : PurchaseRequisitionIn, qp_insert: dict = Depends(qp_insert)):
    purchase_requisitionDict = purchase_requisitionInstance.dict()
    result = await views.post_purchase_requisition(purchase_requisitionDict)
    if qp_insert['nested']:
        query_parametrs_select_one = await qp_select_one(nested=True)
        return await views.get_purchase_requisition_by_id(result['id'], **query_parametrs_select_one)
    return result

@purchase_requisitionRouter.put('/', response_model = Union[PurchaseRequisitionNestedOut,PurchaseRequisitionOut])
async def update_purchase_requisition(purchaseRequisitionIn : PurchaseRequisitionOut, qp_update: dict = Depends(qp_update)):
    purchaseRequisitionInsctance = dict(purchaseRequisitionIn)
    result = await views.update_purchase_requisition(purchaseRequisitionInsctance)
    if qp_update['nested']:
        query_parametrs_select_one = await qp_select_one(nested=True)
        return await views.get_purchase_requisition_by_id(purchaseRequisitionInsctance['id'], **query_parametrs_select_one)
    return purchaseRequisitionInsctance

@purchase_requisitionRouter.delete('/{purchase_requisition_id}')
async def delete_purchase_requisition_by_id(purchase_requisition_id : int):
    result = await views.delete_purchase_requisition_by_id(purchase_requisition_id)
    return result