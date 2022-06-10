from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, add_entity_filter, get_current_active_user
from common_module.urls_module import query_parameters_list, query_parameters
from typing import List, Optional, Union

from catalogs.approval_process.models import ApprovalProcess, ApprovalProcessCheck, ApprovalProcessIn, ApprovalProcessNestedOut, ApprovalProcessOut, ApprovalProcessRoutNestedOut, ApprovalProcessRoutOut, ApprovalProcessRoutPOST, ApprovalProcessRoutPUT, ResponseMapStart
from catalogs.approval_process import views

async def ap_select(document_id: int = 0, document_type_id: int = 0, entity_iin: str = ''):
    return {"document_id": document_id, "document_type_id": document_type_id, "entity_iin": entity_iin}

async def ap_select_list(document_id: list = [], document_type_id: int = 0, entity_iin: str = ''):
    return {"document_id": document_id, "document_type_id": document_type_id, "entity_iin": entity_iin}


approval_processRouter = APIRouter()

@approval_processRouter.get('/start')#, response_model = ResponseMapStart)
async def start_approval_process(process_parameters: dict = Depends(ap_select), parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    result = await views.start_approval_process(process_parameters, **parameters)
    return result

@approval_processRouter.get('/cancel')
async def cancel_approval_process(process_parameters: dict = Depends(ap_select), parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    result = await views.cancel_approval_process(process_parameters, **parameters)
    return result

@approval_processRouter.post('/check')
async def check_many_approval_processes(approvalProcessCheck: ApprovalProcessCheck, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    process_parameters = dict(approvalProcessCheck)
    result = await views.check_approval_processes(process_parameters, **parameters)
    return result

@approval_processRouter.get('/', response_model = Union[list[ApprovalProcessNestedOut], list[ApprovalProcessOut]])
async def get_approval_process_list(parameters: dict = Depends(query_parameters_list), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    records = await views.get_approval_process_list(**parameters)
    return records

@approval_processRouter.get('/{approval_process_id}',  response_model = Union[ApprovalProcessRoutNestedOut, ApprovalProcessRoutOut])
async def get_approval_process_by_id(approval_process_id : int, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    result = await views.get_approval_process_by_id(approval_process_id, **parameters)
    return result

@approval_processRouter.post('/', response_model = ApprovalProcessOut)
async def post_approval_process(approvalProcessRoutPOST : ApprovalProcessRoutPOST, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    approval_processInstanceDict = dict(approvalProcessRoutPOST)
    result = await views.post_approval_process(approval_processInstanceDict, **parameters)
    return result

@approval_processRouter.put('/{approval_process_id}', response_model = ApprovalProcessOut)
async def update_approval_process(approval_process_id : int, approvalProcessRoutPUT : ApprovalProcessRoutPUT, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    approval_processInstanceDict = dict(approvalProcessRoutPUT)
    result = await views.update_approval_process(approval_process_id, approval_processInstanceDict, **parameters)
    return approvalProcessRoutPUT

@approval_processRouter.delete('/{approval_process_id}')
async def delete_approval_process_by_id(approval_process_id : int, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    result = await views.delete_approval_process_by_id(approval_process_id, **parameters)
    return result

