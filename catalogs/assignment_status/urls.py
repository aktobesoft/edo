from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, get_current_active_user
from common_module.urls_module import query_parameters_list

from catalogs.assignment_status.models import AssignmentStatusOut, AssignmentStatusPOST, AssignmentStatusPUT
import catalogs.assignment_status.views as views


assignment_statusRouter = APIRouter()

@assignment_statusRouter.get('/', response_model = list[AssignmentStatusOut])
async def get_assignment_status_list(parameters: dict = Depends(query_parameters_list), current_user: UserModel = Depends(get_current_active_user)):
    records = await views.get_assignment_status_list(**parameters)
    return records

@assignment_statusRouter.get('/{assignment_status_id}')
async def get_assignment_status_by_id(assignment_status_id : int, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.get_assignment_status_by_id(assignment_status_id)
    return result

@assignment_statusRouter.post('/', response_model = AssignmentStatusOut)
async def post_assignment_status(assignment_statusInstance : AssignmentStatusPOST, current_user: UserModel = Depends(get_current_active_user)):
    businessTypeDict = assignment_statusInstance.dict()
    result = await views.post_assignment_status(businessTypeDict)
    return result

@assignment_statusRouter.put('/{assignment_status_id}', response_model = AssignmentStatusOut)
async def update_assignment_status(assignment_status_id : int, AssignmentStatusPUT : AssignmentStatusPUT, current_user: UserModel = Depends(get_current_active_user)):
    newAssignmentStatusPUT = dict(AssignmentStatusPUT)
    result = await views.update_assignment_status(newAssignmentStatusPUT, assignment_status_id)
    return newAssignmentStatusPUT

@assignment_statusRouter.delete('/{assignment_status_id}')
async def delete_assignment_status_by_id(assignment_status_id : int, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.delete_assignment_status_by_id(assignment_status_id)
    return result
