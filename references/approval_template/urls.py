from fastapi import APIRouter, Depends
from common_module.urls_module import qp_select_list
from typing import List, Union

from references.approval_template.models import ApprovalTemplate, ApprovalTemplateIn, ApprovalTemplateOut
from references.approval_template import views


approval_templateRouter = APIRouter()

@approval_templateRouter.get('/', response_model = list[ApprovalTemplateOut])
async def get_approval_template_list(commons: dict = Depends(qp_select_list)):
    records = await views.get_approval_template_list(**commons)
    return records

@approval_templateRouter.get('/{approval_template_id}')
async def get_approval_template_by_id(approval_template_id : int):
    result = await views.get_approval_template_by_id(approval_template_id)
    return result

@approval_templateRouter.post('/', response_model = ApprovalTemplateOut)
async def post_approval_template(approval_templateInstance : ApprovalTemplateIn):
    businessTypeDict = approval_templateInstance.dict()
    result = await views.post_approval_template(businessTypeDict)
    return result

@approval_templateRouter.put('/', response_model = ApprovalTemplateOut)
async def update_approval_template(newApprovalTemplateIn : ApprovalTemplateOut):
    newApprovalTemplateIn = dict(newApprovalTemplateIn)
    result = await views.update_approval_template(newApprovalTemplateIn)
    return newApprovalTemplateIn

@approval_templateRouter.delete('/{approval_template_id}')
async def delete_approval_template_by_id(approval_template_id : int):
    result = await views.delete_approval_template_by_id(approval_template_id)
    return result
