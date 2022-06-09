from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, get_current_active_user
from common_module.urls_module import query_parameters_list, query_parameters
from typing import List, Union

from catalogs.approval_template_step.models import ApprovalTemplateStep, _ApprovalTemplateStepPUT, _ApprovalTemplateStepOut
from catalogs.approval_template_step import views


approval_template_stepRouter = APIRouter()

@approval_template_stepRouter.get('/', response_model = list[_ApprovalTemplateStepOut])
async def get_approval_template_step_list(approval_template_id : int, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    records = await views.get_approval_template_step_list(approval_template_id, **parameters)
    return records

@approval_template_stepRouter.get('/{approval_template_step_id}')
async def get_approval_template_step_by_id(approval_template_step_id : int, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.get_approval_template_step_by_id(approval_template_step_id)
    return result

@approval_template_stepRouter.post('/', response_model = _ApprovalTemplateStepOut)
async def post_approval_template_step(approval_template_stepInstance : _ApprovalTemplateStepPUT, current_user: UserModel = Depends(get_current_active_user)):
    businessTypeDict = approval_template_stepInstance.dict()
    result = await views.post_approval_template_step(businessTypeDict)
    return result

@approval_template_stepRouter.put('/', response_model = _ApprovalTemplateStepOut)
async def update_approval_template_step(newApprovalTemplateStepIn : _ApprovalTemplateStepOut, current_user: UserModel = Depends(get_current_active_user)):
    newApprovalTemplateStepIn = dict(newApprovalTemplateStepIn)
    result = await views.update_approval_template_step(newApprovalTemplateStepIn)
    return newApprovalTemplateStepIn

@approval_template_stepRouter.delete('/{approval_template_step_id}')
async def delete_approval_template_step_by_id(approval_template_step_id : int, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.delete_approval_template_step_by_id(approval_template_step_id)
    return result
