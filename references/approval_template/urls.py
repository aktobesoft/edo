from fastapi import APIRouter, Depends
from common_module.urls_module import qp_select_list, qp_select_one
from typing import List, Union

from references.approval_template.models import ApprovalTemplate, ApprovalTemplateIn, ApprovalTemplateNestedOut,\
                    ApprovalTemplateOut, ApprovalTemplatePOST, ApprovalTemplatePUT, ApprovalTemplateStepOut, ApprovalTemplateStepsNestedOut
from references.approval_template import views


approval_templateRouter = APIRouter()

@approval_templateRouter.get('/', response_model = Union[List[ApprovalTemplateNestedOut], List[ApprovalTemplateOut]])
async def get_approval_template_list(commons: dict = Depends(qp_select_list)):
    records = await views.get_approval_template_list(**commons)
    return records

@approval_templateRouter.get('/{approval_template_id}', response_model = Union[ApprovalTemplateStepsNestedOut, ApprovalTemplateNestedOut, ApprovalTemplateStepOut, ApprovalTemplateOut])
async def get_approval_template_by_id(approval_template_id : int, qp_select_one: dict = Depends(qp_select_one)):
    result = await views.get_approval_template_by_id(approval_template_id, **qp_select_one)
    return result

@approval_templateRouter.post('/', response_model = ApprovalTemplateOut)
async def post_approval_template(item : ApprovalTemplatePOST):
    itemDict = item.dict()
    result = await views.post_approval_template(itemDict)
    return result

@approval_templateRouter.put('/', response_model = ApprovalTemplateOut)
async def update_approval_template(item : ApprovalTemplatePUT):
    itemDict = dict(item)
    result = await views.update_approval_template(itemDict)
    return result

@approval_templateRouter.delete('/{approval_template_id}')
async def delete_approval_template_by_id(approval_template_id : int):
    result = await views.delete_approval_template_by_id(approval_template_id)
    return result
