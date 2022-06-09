from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, get_current_active_user, add_entity_filter, is_entity_allowed
from common_module.urls_module import paginator_execute, query_parameters_list, query_parameters
from documents.base_document.models import OptionsStructure
import catalogs.entity.views as entityService
from catalogs.entity.models import EntityListNestedOut, EntityListOut, EntityOut, EntityIn, EntityNestedOut
from typing import List, Union

entityRouter = APIRouter()


@entityRouter.get('/', response_model = Union[EntityListNestedOut,EntityListOut])
async def get_entity_list(parameters: dict = Depends(query_parameters_list), current_user: UserModel = Depends(get_current_active_user)):
    await add_entity_filter(current_user, parameters)
    await paginator_execute(parameters, await entityService.get_entity_count(**parameters))
    return {'info': parameters, 'result': await entityService.get_entity_list(**parameters)}

@entityRouter.get('/{entity_iin}', response_model=Union[EntityNestedOut,EntityOut])
async def get_entity_by_iin(entity_iin: str, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    await is_entity_allowed(current_user, entity_iin)
    return await entityService.get_entity_by_iin(entity_iin, **parameters)

@entityRouter.post('/', response_model = EntityOut)
async def post_entity(entityInstance : EntityIn, current_user: UserModel = Depends(get_current_active_user)):
    entityDict = entityInstance.dict()
    await is_entity_allowed(current_user, entityDict['iin'])
    result = await entityService.post_entity(entityDict)
    return result

@entityRouter.delete('/{entity_iin}')
async def post_entity(entity_iin: str, current_user: UserModel = Depends(get_current_active_user)):
    await is_entity_allowed(current_user, entity_iin)
    result = await entityService.delete_entity_by_iin(entity_iin)
    return result

@entityRouter.put('/{entity_iin}', response_model = EntityOut)
async def update_entity(entity_iin: str, newEntityIn : EntityOut, current_user: UserModel = Depends(get_current_active_user)):
    newEntityIn = dict(newEntityIn)
    await is_entity_allowed(current_user, newEntityIn['iin'])
    result = await entityService.update_entity(newEntityIn, entity_iin)
    return newEntityIn
