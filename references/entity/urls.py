from fastapi import APIRouter, Depends
from common_module.urls_module import qp_insert, qp_select_list, qp_select_one, qp_update, qp_select_one_by_iin
from documents.base_document.models import OptionsStructure
from references.entity import views
from references.entity.models import EntityOut, EntityIn, EntityNestedOut
from typing import List, Union

entityRouter = APIRouter()


@entityRouter.get('/', response_model = Union[list[EntityNestedOut],list[EntityOut],List[OptionsStructure]])
async def get_entity_list(commons: dict = Depends(qp_select_list)):
    return await views.get_entity_list(**commons)

@entityRouter.get('/{entity_iin}', response_model=EntityOut)
async def get_entity_by_iin(entity_iin: str, qp_select_one: dict = Depends(qp_select_one)):
    return await views.get_entity_by_iin(entity_iin)

@entityRouter.post('/', response_model = EntityOut)
async def post_entity(entityInstance : EntityIn):#, qp_insert: dict = Depends(qp_insert)):
    entityDict = entityInstance.dict()
    result = await views.post_entity(entityDict)
    return result

@entityRouter.delete('/{entity_iin}')
async def post_entity(entity_iin: str):
    result = await views.delete_entity_by_iin(entity_iin)
    return result

@entityRouter.put('/', response_model = EntityOut)
async def update_entity(newEntityIn : EntityOut):#, qp_update: dict = Depends(qp_update)):
    newEntityIn = dict(newEntityIn)
    result = await views.update_entity(newEntityIn)
    return newEntityIn
