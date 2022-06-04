from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, get_current_active_user
from common_module.urls_module import qp_select_list, qp_select_one
from typing import List, Optional, Union

from catalogs.approval_process.models import ApprovalProcess, ApprovalProcessCheck, ApprovalProcessIn, ApprovalProcessNestedOut, ApprovalProcessOut, ApprovalProcessRoutNestedOut, ApprovalProcessRoutOut, ApprovalProcessRoutPOST, ApprovalProcessRoutPUT, ResponseMapStart
from catalogs.approval_process import views

async def ap_select(document_id: int = 0, document_type_id: int = 0, entity_iin: str = ''):
    return {"document_id": document_id, "document_type_id": document_type_id, "entity_iin": entity_iin}

async def ap_select_list(document_id: list = [], document_type_id: int = 0, entity_iin: str = ''):
    return {"document_id": document_id, "document_type_id": document_type_id, "entity_iin": entity_iin}


approval_processRouter = APIRouter()

@approval_processRouter.get('/start')#, response_model = ResponseMapStart)
async def start_approval_process(parameters: dict = Depends(ap_select), current_user: UserModel = Depends(get_current_active_user)):
    result = await views.start_approval_process(parameters)
    return result

@approval_processRouter.get('/cancel')
async def cancel_approval_process(parameters: dict = Depends(ap_select), current_user: UserModel = Depends(get_current_active_user)):
    result = await views.cancel_approval_process(parameters)
    return result

@approval_processRouter.post('/check')
async def check_many_approval_processes(approvalProcessCheck: ApprovalProcessCheck, current_user: UserModel = Depends(get_current_active_user)):
    parameters = dict(approvalProcessCheck)
    result = await views.check_approval_processes(parameters)
    return result

@approval_processRouter.get('/', response_model = Union[list[ApprovalProcessNestedOut], list[ApprovalProcessOut]])
async def get_approval_process_list(commons: dict = Depends(qp_select_list), current_user: UserModel = Depends(get_current_active_user)):
    records = await views.get_approval_process_list(**commons)
    return records

@approval_processRouter.get('/{approval_process_id}',  response_model = Union[ApprovalProcessRoutNestedOut, ApprovalProcessRoutOut])
async def get_approval_process_by_id(approval_process_id : int, parameters: dict = Depends(qp_select_one), current_user: UserModel = Depends(get_current_active_user)):
    result = await views.get_approval_process_by_id(approval_process_id, **parameters)
    return result

@approval_processRouter.post('/', response_model = ApprovalProcessOut)
async def post_approval_process(approvalProcessRoutPOST : ApprovalProcessRoutPOST, current_user: UserModel = Depends(get_current_active_user)):
    approval_processInstanceDict = dict(approvalProcessRoutPOST)
    result = await views.post_approval_process(approval_processInstanceDict)
    return result

@approval_processRouter.put('/{approval_process_id}', response_model = ApprovalProcessOut)
async def update_approval_process(approval_process_id : int, approvalProcessRoutPUT : ApprovalProcessRoutPUT, current_user: UserModel = Depends(get_current_active_user)):
    approval_processInstanceDict = dict(approvalProcessRoutPUT)
    result = await views.update_approval_process(approval_process_id, approval_processInstanceDict)
    return approvalProcessRoutPUT

@approval_processRouter.delete('/{approval_process_id}')
async def delete_approval_process_by_id(approval_process_id : int, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.delete_approval_process_by_id(approval_process_id)
    return result

