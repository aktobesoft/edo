from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, add_parameters, add_entity_filter, get_current_active_user
from common_module.urls_module import approval_parameters, paginator_execute, query_parameters_list, query_parameters, query_parameters
from typing import Union

from documents.purchase_requisition.models import PurchaseRequisitionNestedItemsOut, PurchaseRequisitionNestedItemsOutWithRoutes, PurchaseRequisitionPUT,\
        PurchaseRequisitionPOST, PurchaseRequisitionItemsOut
import documents.purchase_requisition.views as views

purchase_requisitionRouter = APIRouter()

@purchase_requisitionRouter.get('/')
async def get_purchase_requisition_list(parameters: dict = Depends(query_parameters_list), 
                approvalParameters: dict = Depends(approval_parameters),current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    await add_parameters(approvalParameters, parameters)
    await paginator_execute(parameters, await views.get_purchase_requisition_count(**parameters))
    return {'info': parameters, 'result': await views.get_purchase_requisition_list(**parameters)}

@purchase_requisitionRouter.get('/{purchase_requisition_id}',response_model = Union[PurchaseRequisitionNestedItemsOutWithRoutes,PurchaseRequisitionNestedItemsOut, PurchaseRequisitionItemsOut])
async def get_purchase_requisition_by_id(purchase_requisition_id : int, approvalParameters: dict = Depends(approval_parameters), 
    parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    await add_parameters(approvalParameters, parameters)
    result = await views.get_purchase_requisition_by_id(purchase_requisition_id, **parameters)
    return result

@purchase_requisitionRouter.post('/', response_model = Union[PurchaseRequisitionNestedItemsOut, PurchaseRequisitionPOST])
async def post_purchase_requisition(purchase_requisitionInstance : PurchaseRequisitionPOST, parameters: dict = Depends(query_parameters)\
                            , current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    purchase_requisitionDict = purchase_requisitionInstance.dict()
    result = await views.post_purchase_requisition(purchase_requisitionDict, **parameters)
    if parameters['nested']:
        return await views.get_purchase_requisition_by_id(result['id'], **parameters)
    return result

@purchase_requisitionRouter.put('/{purchase_requisition_id}', response_model = Union[PurchaseRequisitionNestedItemsOut, PurchaseRequisitionItemsOut])
async def update_purchase_requisition(purchase_requisition_id: int, PurchaseRequisitionPUT : PurchaseRequisitionPUT, parameters: dict = Depends(query_parameters)\
                            , current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    purchaseRequisitionInsctance = dict(PurchaseRequisitionPUT)
    result = await views.update_purchase_requisition(purchaseRequisitionInsctance, purchase_requisition_id, **parameters)
    if parameters['nested']:
        return await views.get_purchase_requisition_by_id(purchase_requisition_id, **parameters)
    return purchaseRequisitionInsctance

@purchase_requisitionRouter.delete('/{purchase_requisition_id}')
async def delete_purchase_requisition_by_id(purchase_requisition_id : int, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    return await views.delete_purchase_requisition_by_id(purchase_requisition_id, **parameters)