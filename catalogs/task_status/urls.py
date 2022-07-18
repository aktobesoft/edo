from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, add_entity_filter, get_current_active_user
from common_module.urls_module import query_parameters, query_parameters_list

from catalogs.task_status.models import TaskStatusOut, TaskStatusPOST, TaskStatusPUT
import catalogs.task_status.views as views


task_statusRouter = APIRouter()

@task_statusRouter.get('/', response_model = list[TaskStatusOut])
async def get_task_status_list(parameters: dict = Depends(query_parameters_list), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    records = await views.get_task_status_list(**parameters)
    return records

@task_statusRouter.get('/{task_status_id}')
async def get_task_status_by_id(task_status_id : int, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    result = await views.get_task_status_by_id(task_status_id, **parameters)
    return result

@task_statusRouter.post('/', response_model = TaskStatusOut)
async def post_task_status(task_statusInstance : TaskStatusPOST, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    taskStatusDict = task_statusInstance.dict()
    result = await views.post_task_status(taskStatusDict, **parameters)
    return result

@task_statusRouter.put('/{task_status_id}', response_model = TaskStatusOut)
async def update_task_status(task_status_id : int, TaskStatusPUT : TaskStatusPUT, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    newTaskStatusPUT = dict(TaskStatusPUT)
    result = await views.update_task_status(newTaskStatusPUT, task_status_id, **parameters)
    return newTaskStatusPUT

@task_statusRouter.delete('/{task_status_id}')
async def delete_task_status_by_id(task_status_id : int, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    result = await views.delete_task_status_by_id(task_status_id, **parameters)
    return result
