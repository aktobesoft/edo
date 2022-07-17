from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, get_current_active_user
from common_module.urls_module import query_parameters_list

from catalogs.task_status.models import TaskStatusOut, TaskStatusPOST, TaskStatusPUT
import catalogs.task_status.views as views


task_statusRouter = APIRouter()

@task_statusRouter.get('/', response_model = list[TaskStatusOut])
async def get_task_status_list(parameters: dict = Depends(query_parameters_list), current_user: UserModel = Depends(get_current_active_user)):
    records = await views.get_task_status_list(**parameters)
    return records

@task_statusRouter.get('/{task_status_id}')
async def get_task_status_by_id(task_status_id : int, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.get_task_status_by_id(task_status_id)
    return result

@task_statusRouter.post('/', response_model = TaskStatusOut)
async def post_task_status(task_statusInstance : TaskStatusPOST, current_user: UserModel = Depends(get_current_active_user)):
    businessTypeDict = task_statusInstance.dict()
    result = await views.post_task_status(businessTypeDict)
    return result

@task_statusRouter.put('/{task_status_id}', response_model = TaskStatusOut)
async def update_task_status(task_status_id : int, TaskStatusPUT : TaskStatusPUT, current_user: UserModel = Depends(get_current_active_user)):
    newTaskStatusPUT = dict(TaskStatusPUT)
    result = await views.update_task_status(newTaskStatusPUT, task_status_id)
    return newTaskStatusPUT

@task_statusRouter.delete('/{task_status_id}')
async def delete_task_status_by_id(task_status_id : int, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.delete_task_status_by_id(task_status_id)
    return result
