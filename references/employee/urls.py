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
    newEmployee = await views.post_employee(newEmployeeIn)
    return newEmployee

@employeeRouter.delete('/{employee_id}')
async def post_employee(employee_id : int):
    newEmployee = await views.delete_employee_by_id(employee_id)
    return newEmployee

@employeeRouter.put('/', response_model = EmployeeOut)
async def update_employee(newEmployeeIn : EmployeeOut):
    newEmployeeIn = dict(newEmployeeIn)
    newEmployee = await views.update_employee(newEmployeeIn['id'], newEmployeeIn)
    newEmployee = await views.get_employee_by_id(newEmployeeIn['id'])
    return newEmployee