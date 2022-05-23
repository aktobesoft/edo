from fastapi import APIRouter, Depends
from common_module.urls_module import paginator_execute, qp_select_list
from catalogs.employee import views
from catalogs.employee.models import EmployeeListNestedOut, EmployeeListOut, EmployeeOut, EmployeeIn
from typing import List, Union
from documents.base_document.models import OptionsStructure

employeeRouter = APIRouter()

@employeeRouter.get('/', response_model = Union[EmployeeListNestedOut, EmployeeListOut])
async def get_employee_list(query_param: dict = Depends(qp_select_list)):
    parametrs = await paginator_execute(query_param, await views.get_employee_count())
    return {'info': parametrs, 'result': await views.get_employee_list(**parametrs)}

@employeeRouter.get('/{employee_id}', response_model=EmployeeOut)
async def get_employee_by_id(employee_id: int):
    return await views.get_employee_by_id(employee_id)

@employeeRouter.post('/', response_model = EmployeeOut)
async def post_employee(newEmployeeIn : EmployeeIn):
    result = await views.post_employee(newEmployeeIn.dict())
    return result

@employeeRouter.delete('/{employee_id}')
async def delete_employee_by_id(employee_id : int):
    result = await views.delete_employee_by_id(employee_id)
    return result

@employeeRouter.put('/{employee_id}', response_model = EmployeeOut)
async def update_employee(newEmployeeIn : EmployeeOut, employee_id: int):
    result = await views.update_employee(newEmployeeIn.dict(), employee_id)
    return result