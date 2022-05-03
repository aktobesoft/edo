from fastapi import APIRouter, Depends
from common_module.urls_module import qp_select_list
from typing import List, Union

from references.approval_template_step.models import ApprovalTemplateStep, ApprovalTemplateStepIn, ApprovalTemplateStepOut
from references.approval_template_step import views


approval_template_stepRouter = APIRouter()

@approval_template_stepRouter.get('/', response_model = list[ApprovalTemplateStepOut])
async def get_approval_template_step_list(commons: dict = Depends(qp_select_list)):
    records = await views.get_approval_template_step_list(**commons)
    return records

@approval_template_stepRouter.get('/{approval_template_step_id}')
async def get_approval_template_step_by_id(approval_template_step_id : int):
    result = await views.get_approval_template_step_by_id(approval_template_step_id)
    return result

@approval_template_stepRouter.post('/', response_model = ApprovalTemplateStepOut)
async def post_approval_template_step(approval_template_stepInstance : ApprovalTemplateStepIn):
    businessTypeDict = approval_template_stepInstance.dict()
    result = await views.post_approval_template_step(businessTypeDict)
    return result

@approval_template_stepRouter.put('/', response_model = ApprovalTemplateStepOut)
async def update_approval_template_step(newApprovalTemplateStepIn : ApprovalTemplateStepOut):
    newApprovalTemplateStepIn = dict(newApprovalTemplateStepIn)
    result = await views.update_approval_template_step(newApprovalTemplateStepIn)
    return newApprovalTemplateStepIn

@approval_template_stepRouter.delete('/{approval_template_step_id}')
async def delete_approval_template_step_by_id(approval_template_step_id : int):
    result = await views.delete_approval_template_step_by_id(approval_template_step_id)
    return result
