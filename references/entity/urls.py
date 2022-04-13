from fastapi import APIRouter, Depends
from common_module.urls_module import common_parameters
from references.entity import views
from references.entity.models import EntityOut, EntityIn, EntityOptionsOut, EntityNestedOut
from typing import List

entityRouter = APIRouter()


@entityRouter.get('/', response_model=list[EntityOut])
async def get_entity_list(commons: dict = Depends(common_parameters)):
    return await views.get_entity_list(**commons)

@entityRouter.get('/{entity_id}', response_model=EntityOut)
async def get_entity_by_id(entity_id: int):
    return await views.get_entity_by_id(entity_id)

@entityRouter.post('/', response_model = EntityOut)
async def post_entity(entityInstance : EntityIn):
    entityDict = entityInstance.dict()
    result = await views.post_entity(entityDict)
    return result

@entityRouter.delete('/{entity_id}')
async def post_entity(entity_id : int):
    result = await views.delete_entity_by_id(entity_id)
    return result

@entityRouter.put('/', response_model = EntityOut)
async def update_entity(newEntityIn : EntityOut):
    newEntityIn = dict(newEntityIn)
    result = await views.update_entity(newEntityIn)
    return newEntityIn

@entityRouter.get('/options/', response_model = List[EntityOptionsOut])
async def get_entity_options_list(commons: dict = Depends(common_parameters)):
    listValue = await views.get_entity_options_list(**commons)
    return listValue