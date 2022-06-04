from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, get_current_active_user
from common_module.urls_module import paginator_execute, qp_select_list
from documents.base_document.models import OptionsStructure
from core.db import database
from sqlalchemy import select
from typing import List, Union

from catalogs.user.models import UserListOut, UserOut, UserPOST, UserPUT
import catalogs.user.views as userService

userRouter = APIRouter()

@userRouter.get('/', response_model = UserListOut)
async def get_user_list(parameters: dict = Depends(qp_select_list), current_user: UserModel = Depends(get_current_active_user)):
    await paginator_execute(parameters, await userService.get_user_count())
    return {'info': parameters, 'result': await userService.get_user_list(**parameters)}

@userRouter.get('/{user_id}', response_model = Union[UserOut, OptionsStructure])
async def get_user_by_id(user_id: int, current_user: UserModel = Depends(get_current_active_user)):
    listValue = await userService.get_user_by_id(user_id)
    return listValue

@userRouter.post('/', response_model = UserOut)
async def post_user(newUser : UserPOST, current_user: UserModel = Depends(get_current_active_user)):
    newUser = dict(newUser)
    newUser_id = await userService.post_user(newUser)
    return {**newUser, 'id': int(newUser_id)}

@userRouter.delete('/{user_id}')
async def delete_user(user_id: int, current_user: UserModel = Depends(get_current_active_user)):
    result = await userService.delete_user_by_id(user_id)
    return result

@userRouter.put('/{user_id}', response_model = UserPUT)
async def update_user(user_id: int, newUser : UserPUT, current_user: UserModel = Depends(get_current_active_user)):#, qp_update: dict = Depends(qp_update)):
    newUser_ = dict(newUser)
    result = await userService.update_user(newUser_, user_id)
    return newUser_
