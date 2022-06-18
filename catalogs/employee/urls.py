from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, add_entity_filter, get_current_active_user
from common_module.urls_module import paginator_execute, query_parameters_list, query_parameters
from catalogs.employee import views
from catalogs.employee.models import EmployeeListNestedOut, EmployeeListOut, EmployeeOut, EmployeeIn
from typing import List, Union
from documents.base_document.models import OptionsStructure

employeeRouter = APIRouter()

@employeeRouter.get('/', response_model = Union[EmployeeListNestedOut, EmployeeListOut])
async def get_employee_list(parameters: dict = Depends(query_parameters_list), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    await paginator_execute(parameters, await views.get_employee_count(**parameters))
    return {'info': parameters, 'result': await views.get_employee_list(**parameters)}

@employeeRouter.get('/{employee_id}', response_model=EmployeeOut)
async def get_employee_by_id(employee_id: int, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    return await views.get_employee_by_id(employee_id, **parameters)

@employeeRouter.post('/', response_model = EmployeeOut)
async def post_employee(newEmployeeIn : EmployeeIn, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    result = await views.post_employee(newEmployeeIn.dict(), **parameters)
    return result

@employeeRouter.delete('/{employee_id}')
async def delete_employee_by_id(employee_id : int, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    result = await views.delete_employee_by_id(employee_id, **parameters)
    return result

@employeeRouter.put('/{employee_id}', response_model = EmployeeOut)
async def update_employee(newEmployeeIn : EmployeeOut, employee_id: int, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    result = await views.update_employee(newEmployeeIn.dict(), employee_id, **parameters)
    return result