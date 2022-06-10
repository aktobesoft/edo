from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, add_entity_filter, get_current_active_user
from common_module.urls_module import query_parameters_list, query_parameters
from typing import List, Union

from catalogs.approval_template.models import ApprovalTemplate, ApprovalTemplateIn, ApprovalTemplateNestedOut,\
                    ApprovalTemplateOut, ApprovalTemplatePOST, ApprovalTemplatePUT, ApprovalTemplateStepOut, ApprovalTemplateStepsNestedOut
from catalogs.approval_template import views


approval_templateRouter = APIRouter()

@approval_templateRouter.get('/', response_model = Union[List[ApprovalTemplateNestedOut], List[ApprovalTemplateOut]])
async def get_approval_template_list(parameters: dict = Depends(query_parameters_list), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    records = await views.get_approval_template_list(**parameters)
    return records

@approval_templateRouter.get('/{approval_template_id}', response_model = Union[ApprovalTemplateStepsNestedOut, ApprovalTemplateNestedOut, ApprovalTemplateStepOut, ApprovalTemplateOut])
async def get_approval_template_by_id(approval_template_id : int, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    result = await views.get_approval_template_by_id(approval_template_id, **parameters)
    return result

@approval_templateRouter.post('/', response_model = ApprovalTemplateOut)
async def post_approval_template(item : ApprovalTemplatePOST, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    itemDict = item.dict()
    result = await views.post_approval_template(itemDict, **parameters)
    return result

@approval_templateRouter.put('/{approval_template_id}', response_model = ApprovalTemplateOut)
async def update_approval_template(approval_template_id : int, item : ApprovalTemplatePUT, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    itemDict = dict(item)
    result = await views.update_approval_template(itemDict, approval_template_id, **parameters)
    return result

@approval_templateRouter.delete('/{approval_template_id}')
async def delete_approval_template_by_id(approval_template_id : int, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    result = await views.delete_approval_template_by_id(approval_template_id, **parameters)
    return result
