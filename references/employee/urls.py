from fastapi import APIRouter, Depends
from common_module.urls_module import qp_select_list
from references.employee import views
from references.employee.models import EmployeeOut, EmployeeIn, EmployeeNestedOut
from typing import List, Union
from documents.base_document.models import OptionsStructure

employeeRouter = APIRouter()

@employeeRouter.get('/', response_model = Union[list[EmployeeNestedOut], list[EmployeeOut], List[OptionsStructure]])
async def get_employee_list(commons: dict = Depends(qp_select_list)):
    return await views.get_employee_list(**commons)

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

@employeeRouter.put('/', response_model = EmployeeOut)
async def update_employee(newEmployeeIn : EmployeeOut):
    result = await views.update_employee(newEmployeeIn.dict())
    return result