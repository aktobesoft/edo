from fastapi import APIRouter, Depends
from common_module.urls_module import common_parameters
from references.entity import views as entityService
from references.entity.models import EntityOut, EntityIn, EntityOptionsOut
from typing import List

entityRouter = APIRouter()


@entityRouter.get('/', response_model=list[EntityOut])
async def get_entity_list(commons: dict = Depends(common_parameters)):
    return await entityService.get_entity_list(**commons)

@entityRouter.get('/{entity_id}', response_model=EntityOut)
async def get_entity_by_id(entity_id: int):
    return await entityService.get_entity_by_id(entity_id)

@entityRouter.post('/', response_model = EntityOut)
async def post_entity(newEntityIn : EntityIn):
    newEntity = await entityService.post_entity(newEntityIn)
    return newEntity

@entityRouter.delete('/{entity_id}')
async def post_entity(entity_id : int):
    newEntity = await entityService.delete_entity_by_id(entity_id)
    return newEntity

@entityRouter.put('/', response_model = EntityOut)
async def update_entity(newEntityIn : EntityOut):
    newEntityIn = dict(newEntityIn)
    newEntity = await entityService.update_entity(newEntityIn['id'], newEntityIn)
    newEntity = await entityService.get_entity_by_id(newEntityIn['id'])
    return newEntity

@entityRouter.get('/options/', response_model = List[EntityOptionsOut])
async def get_entity_options_list(commons: dict = Depends(common_parameters)):
    listValue = await entityService.get_entity_options_list(**commons)
    return listValue