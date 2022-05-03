from fastapi import APIRouter, Depends
from common_module.urls_module import qp_select_list
from typing import List, Union

from references.approval_process.models import ApprovalProcess, ApprovalProcessIn, ApprovalProcessOut
from references.approval_process import views


approval_processRouter = APIRouter()

@approval_processRouter.get('/', response_model = list[ApprovalProcessOut])
async def get_approval_process_list(commons: dict = Depends(qp_select_list)):
    records = await views.get_approval_process_list(**commons)
    return records

@approval_processRouter.get('/{approval_process_id}')
async def get_approval_process_by_id(approval_process_id : int):
    result = await views.get_approval_process_by_id(approval_process_id)
    return result

@approval_processRouter.post('/', response_model = ApprovalProcessOut)
async def post_approval_process(approval_processInstance : ApprovalProcessIn):
    businessTypeDict = approval_processInstance.dict()
    result = await views.post_approval_process(businessTypeDict)
    return result

@approval_processRouter.put('/', response_model = ApprovalProcessOut)
async def update_approval_process(newApprovalProcessIn : ApprovalProcessOut):
    newApprovalProcessIn = dict(newApprovalProcessIn)
    result = await views.update_approval_process(newApprovalProcessIn)
    return newApprovalProcessIn

@approval_processRouter.delete('/{approval_process_id}')
async def delete_approval_process_by_id(approval_process_id : int):
    result = await views.delete_approval_process_by_id(approval_process_id)
    return result
