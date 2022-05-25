from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, get_current_active_user
from common_module.urls_module import qp_select_list
from documents.base_document.models import OptionsStructure
from core.db import database
from sqlalchemy import select
from typing import List, Union

from catalogs.entity.models import EntityOut, EntityIn
from catalogs.user.models import UserOptionsOut, UserOut, UserIn
from catalogs.user import views as userService

userRouter = APIRouter()

@userRouter.get('/', response_model = Union[List[UserOut], List[OptionsStructure]])
async def get_user_list(commons: dict = Depends(qp_select_list), current_user: UserModel = Depends(get_current_active_user)):
    listValue = await userService.get_user_list(**commons)
    return listValue

@userRouter.post('/', response_model = UserOut)
async def post_user(newUser : UserIn):
    newUser = await userService.post_user(newUser)
    return dict(newUser)