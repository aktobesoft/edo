from fastapi import APIRouter, Depends
from common_module.urls_module import qp_select_list, qp_select_one
from typing import List, Union

from references.approval_template_step.models import ApprovalTemplateStep, _ApprovalTemplateStepIn, _ApprovalTemplateStepOut
from references.approval_template_step import views


approval_template_stepRouter = APIRouter()

@approval_template_stepRouter.get('/', response_model = list[_ApprovalTemplateStepOut])
async def get_approval_template_step_list(approval_template_id : int, qp_select_one: dict = Depends(qp_select_one)):
    records = await views.get_approval_template_step_list(approval_template_id, **qp_select_one)
    return records

@approval_template_stepRouter.get('/{approval_template_step_id}')
async def get_approval_template_step_by_id(approval_template_step_id : int):
    result = await views.get_approval_template_step_by_id(approval_template_step_id)
    return result

@approval_template_stepRouter.post('/', response_model = _ApprovalTemplateStepOut)
async def post_approval_template_step(approval_template_stepInstance : _ApprovalTemplateStepIn):
    businessTypeDict = approval_template_stepInstance.dict()
    result = await views.post_approval_template_step(businessTypeDict)
    return result

@approval_template_stepRouter.put('/', response_model = _ApprovalTemplateStepOut)
async def update_approval_template_step(newApprovalTemplateStepIn : _ApprovalTemplateStepOut):
    newApprovalTemplateStepIn = dict(newApprovalTemplateStepIn)
    result = await views.update_approval_template_step(newApprovalTemplateStepIn)
    return newApprovalTemplateStepIn

@approval_template_stepRouter.delete('/{approval_template_step_id}')
async def delete_approval_template_step_by_id(approval_template_step_id : int):
    result = await views.delete_approval_template_step_by_id(approval_template_step_id)
    return result
