from fastapi import APIRouter, Depends
from common_module.urls_module import common_parameters
from references.employee import views
from references.employee.models import EmployeeOut, EmployeeIn
from typing import List

employeeRouter = APIRouter()

@employeeRouter.get('/', response_model=list[EmployeeOut])
async def get_employee_list(commons: dict = Depends(common_parameters)):
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