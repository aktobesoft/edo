from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, add_approval_filter, add_entity_filter, get_current_active_user
from common_module.urls_module import approval_parameters, paginator_execute, query_parameters_list, query_parameters, query_parameters
from typing import Union

from documents.employee_task.models import EmployeeTaskNestedOut, EmployeeTaskPUT, EmployeeTaskPOST, EmployeeTaskOut
import documents.employee_task.views as views

employee_taskRouter = APIRouter()

@employee_taskRouter.get('/')
async def get_employee_task_list(parameters: dict = Depends(query_parameters_list), 
                approvalParameters: dict = Depends(approval_parameters),current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    await add_approval_filter(approvalParameters, parameters)
    await paginator_execute(parameters, await views.get_employee_task_count(**parameters))
    return {'info': parameters, 'result': await views.get_employee_task_list(**parameters)}

@employee_taskRouter.get('/{employee_task_id}',response_model = Union[EmployeeTaskNestedOut, EmployeeTaskOut])
async def get_employee_task_by_id(employee_task_id : int, approvalParameters: dict = Depends(approval_parameters), 
    parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    await add_approval_filter(approvalParameters, parameters)
    result = await views.get_employee_task_by_id(employee_task_id, **parameters)
    return result

@employee_taskRouter.post('/', response_model = Union[EmployeeTaskNestedOut, EmployeeTaskPOST])
async def post_employee_task(employee_taskInstance : EmployeeTaskPOST, parameters: dict = Depends(query_parameters)\
                            , current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    employee_taskDict = employee_taskInstance.dict()
    result = await views.post_employee_task(employee_taskDict, **parameters)
    if parameters['nested']:
        return await views.get_employee_task_by_id(result['id'], **parameters)
    return result

@employee_taskRouter.put('/{employee_task_id}', response_model = Union[EmployeeTaskNestedOut, EmployeeTaskOut])
async def update_employee_task(employee_task_id: int, EmployeeTaskPUT : EmployeeTaskPUT, parameters: dict = Depends(query_parameters)\
                            , current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    employeeTaskInsctance = dict(EmployeeTaskPUT)
    result = await views.update_employee_task(employeeTaskInsctance, employee_task_id, **parameters)
    if parameters['nested']:
        return await views.get_employee_task_by_id(employee_task_id, **parameters)
    return employeeTaskInsctance

@employee_taskRouter.delete('/{employee_task_id}')
async def delete_employee_task_by_id(employee_task_id : int, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    return await views.delete_employee_task_by_id(employee_task_id, **parameters)