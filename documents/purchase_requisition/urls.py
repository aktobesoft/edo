from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, get_current_active_user
from common_module.urls_module import paginator_execute, qp_select_list, qp_select_one, qp_update, qp_insert
from typing import List, Union

from documents.purchase_requisition.models import PurchaseRequisitionListNestedOut, PurchaseRequisitionListOut, PurchaseRequisitionNestedItemsOut, PurchaseRequisitionPUT,\
        PurchaseRequisitionPOST, PurchaseRequisitionNestedOut, PurchaseRequisitionOut, PurchaseRequisitionItemsOut
import documents.purchase_requisition.views as views
from documents.purchase_requisition_items.models import _PurchaseRequisitionItemsPOST


purchase_requisitionRouter = APIRouter()

@purchase_requisitionRouter.get('/', response_model = Union[PurchaseRequisitionListNestedOut, PurchaseRequisitionListOut])
async def get_purchase_requisition_list(parameters: dict = Depends(qp_select_list), current_user: UserModel = Depends(get_current_active_user)):
    await paginator_execute(parameters, await views.get_purchase_requisition_count())
    return {'info': parameters, 'result': await views.get_purchase_requisition_list(**parameters)}

@purchase_requisitionRouter.get('/{purchase_requisition_id}',response_model = Union[PurchaseRequisitionNestedItemsOut, PurchaseRequisitionItemsOut])
async def get_purchase_requisition_by_id(purchase_requisition_id : int, parameters: dict = Depends(qp_select_one), current_user: UserModel = Depends(get_current_active_user)):
    result = await views.get_purchase_requisition_by_id(purchase_requisition_id, **parameters)
    return result

@purchase_requisitionRouter.post('/', response_model = Union[PurchaseRequisitionNestedItemsOut, PurchaseRequisitionPOST])
async def post_purchase_requisition(purchase_requisitionInstance : PurchaseRequisitionPOST, qp_insert: dict = Depends(qp_insert)\
    , current_user: UserModel = Depends(get_current_active_user)):
    purchase_requisitionDict = purchase_requisitionInstance.dict()
    result = await views.post_purchase_requisition(purchase_requisitionDict)
    if qp_insert['nested']:
        parameters = await qp_select_one(nested=True)
        return await views.get_purchase_requisition_by_id(result['id'], **parameters)
    return result

@purchase_requisitionRouter.put('/{purchase_requisition_id}', response_model = Union[PurchaseRequisitionNestedItemsOut, PurchaseRequisitionItemsOut])
async def update_purchase_requisition(purchase_requisition_id: int, PurchaseRequisitionPUT : PurchaseRequisitionPUT, qp_update: dict = Depends(qp_update)\
    , current_user: UserModel = Depends(get_current_active_user)):
    purchaseRequisitionInsctance = dict(PurchaseRequisitionPUT)
    result = await views.update_purchase_requisition(purchaseRequisitionInsctance, purchase_requisition_id)
    if qp_update['nested']:
        parameters = await qp_select_one(nested=True)
        return await views.get_purchase_requisition_by_id(purchase_requisition_id, **parameters)
    return purchaseRequisitionInsctance

@purchase_requisitionRouter.delete('/{purchase_requisition_id}')
async def delete_purchase_requisition_by_id(purchase_requisition_id : int, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.delete_purchase_requisition_by_id(purchase_requisition_id)
    return result