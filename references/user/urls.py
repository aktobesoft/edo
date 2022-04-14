from fastapi import APIRouter, Depends
from common_module.urls_module import common_parameters
from documents.base_document.models import OptionsStructure
from core.db import database
from sqlalchemy import select
from typing import List, Union

from references.entity.models import EntityOut, EntityIn
from references.user.models import UserOptionsOut, UserOut, UserIn
from references.user import views as userService

userRouter = APIRouter()

@userRouter.get('/', response_model = Union[List[UserOut], List[OptionsStructure]])
async def get_user_list(commons: dict = Depends(common_parameters)):
    listValue = await userService.get_user_list(**commons)
    return listValue

@userRouter.post('/', response_model = UserOut)
async def post_user(newUser : UserIn):
    newUser = await userService.post_user(newUser)
    return dict(newUser)