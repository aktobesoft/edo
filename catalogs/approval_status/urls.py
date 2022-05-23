from fastapi import APIRouter, Depends
from common_module.urls_module import qp_select_list

from catalogs.approval_status.models import ApprovalStatusOut, ApprovalStatusPOST, ApprovalStatusPUT
from catalogs.approval_status import views


approval_statusRouter = APIRouter()

@approval_statusRouter.get('/', response_model = list[ApprovalStatusOut])
async def get_approval_status_list(commons: dict = Depends(qp_select_list)):
    records = await views.get_approval_status_list(**commons)
    return records

@approval_statusRouter.get('/{approval_status_id}')
async def get_approval_status_by_id(approval_status_id : int):
    result = await views.get_approval_status_by_id(approval_status_id)
    return result

@approval_statusRouter.post('/', response_model = ApprovalStatusOut)
async def post_approval_status(approval_statusInstance : ApprovalStatusPOST):
    businessTypeDict = approval_statusInstance.dict()
    result = await views.post_approval_status(businessTypeDict)
    return result

@approval_statusRouter.put('/{approval_status_id}', response_model = ApprovalStatusOut)
async def update_approval_status(approval_status_id : int, ApprovalStatusPUT : ApprovalStatusPUT):
    newApprovalStatusPUT = dict(ApprovalStatusPUT)
    result = await views.update_approval_status(newApprovalStatusPUT, approval_status_id)
    return newApprovalStatusPUT

@approval_statusRouter.delete('/{approval_status_id}')
async def delete_approval_status_by_id(approval_status_id : int):
    result = await views.delete_approval_status_by_id(approval_status_id)
    return result
