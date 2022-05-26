from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, get_current_active_user
from common_module.urls_module import qp_select_list, qp_select_one
from typing import List, Union

from catalogs.approval_template.models import ApprovalTemplate, ApprovalTemplateIn, ApprovalTemplateNestedOut,\
                    ApprovalTemplateOut, ApprovalTemplatePOST, ApprovalTemplatePUT, ApprovalTemplateStepOut, ApprovalTemplateStepsNestedOut
from catalogs.approval_template import views


approval_templateRouter = APIRouter()

@approval_templateRouter.get('/', response_model = Union[List[ApprovalTemplateNestedOut], List[ApprovalTemplateOut]])
async def get_approval_template_list(commons: dict = Depends(qp_select_list), current_user: UserModel = Depends(get_current_active_user)):
    records = await views.get_approval_template_list(**commons)
    return records

@approval_templateRouter.get('/{approval_template_id}', response_model = Union[ApprovalTemplateStepsNestedOut, ApprovalTemplateNestedOut, ApprovalTemplateStepOut, ApprovalTemplateOut])
async def get_approval_template_by_id(approval_template_id : int, qp_select_one: dict = Depends(qp_select_one), current_user: UserModel = Depends(get_current_active_user)):
    result = await views.get_approval_template_by_id(approval_template_id, **qp_select_one)
    return result

@approval_templateRouter.post('/', response_model = ApprovalTemplateOut)
async def post_approval_template(item : ApprovalTemplatePOST, current_user: UserModel = Depends(get_current_active_user)):
    itemDict = item.dict()
    result = await views.post_approval_template(itemDict)
    return result

@approval_templateRouter.put('/{approval_template_id}', response_model = ApprovalTemplateOut)
async def update_approval_template(approval_template_id : int, item : ApprovalTemplatePUT, current_user: UserModel = Depends(get_current_active_user)):
    itemDict = dict(item)
    result = await views.update_approval_template(itemDict, approval_template_id)
    return result

@approval_templateRouter.delete('/{approval_template_id}')
async def delete_approval_template_by_id(approval_template_id : int, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.delete_approval_template_by_id(approval_template_id)
    return result
