from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, get_current_active_user
from common_module.urls_module import query_parameters_list

from catalogs.approval_status.models import ApprovalStatusOut, ApprovalStatusPOST, ApprovalStatusPUT
from catalogs.approval_status import views


approval_statusRouter = APIRouter()

@approval_statusRouter.get('/', response_model = list[ApprovalStatusOut])
async def get_approval_status_list(parameters: dict = Depends(query_parameters_list), current_user: UserModel = Depends(get_current_active_user)):
    records = await views.get_approval_status_list(**parameters)
    return records

@approval_statusRouter.get('/{approval_status_id}')
async def get_approval_status_by_id(approval_status_id : int, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.get_approval_status_by_id(approval_status_id)
    return result

@approval_statusRouter.post('/', response_model = ApprovalStatusOut)
async def post_approval_status(approval_statusInstance : ApprovalStatusPOST, current_user: UserModel = Depends(get_current_active_user)):
    businessTypeDict = approval_statusInstance.dict()
    result = await views.post_approval_status(businessTypeDict)
    return result

@approval_statusRouter.put('/{approval_status_id}', response_model = ApprovalStatusOut)
async def update_approval_status(approval_status_id : int, ApprovalStatusPUT : ApprovalStatusPUT, current_user: UserModel = Depends(get_current_active_user)):
    newApprovalStatusPUT = dict(ApprovalStatusPUT)
    result = await views.update_approval_status(newApprovalStatusPUT, approval_status_id)
    return newApprovalStatusPUT

@approval_statusRouter.delete('/{approval_status_id}')
async def delete_approval_status_by_id(approval_status_id : int, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.delete_approval_status_by_id(approval_status_id)
    return result
