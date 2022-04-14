from fastapi import APIRouter, Depends
from common_module.urls_module import common_parameters
from documents.base_document.models import OptionsStructure
from references.entity import views
from references.entity.models import EntityOut, EntityIn, EntityNestedOut
from typing import List, Union

entityRouter = APIRouter()


@entityRouter.get('/', response_model = Union[list[EntityNestedOut],list[EntityOut],List[OptionsStructure]])
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
