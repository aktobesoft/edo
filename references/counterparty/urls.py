from fastapi import APIRouter, Depends
from common_module.urls_module import common_parameters
from references.counterparty import views
from documents.base_document.models import OptionsStructure
from references.counterparty.models import CounterpartyOut, CounterpartyIn, CounterpartyNestedOut
from typing import List, Union

counterpartyRouter = APIRouter()

@counterpartyRouter.get('/', response_model=Union[list[CounterpartyNestedOut],List[CounterpartyOut], list[OptionsStructure]])
async def get_counterparty_list(commons: dict = Depends(common_parameters)):
    return await views.get_counterparty_list(**commons)

@counterpartyRouter.get('/{counterparty_id}', response_model=CounterpartyOut)
async def get_counterparty_by_id(counterparty_id: int):
    return await views.get_counterparty_by_id(counterparty_id)

@counterpartyRouter.post('/', response_model = CounterpartyOut)
async def post_counterparty(newCounterpartyIn : CounterpartyIn):
    result = await views.post_counterparty(newCounterpartyIn.dict())
    return result

@counterpartyRouter.delete('/{counterparty_id}')
async def delete_counterparty_by_id(counterparty_id : int):
    result = await views.delete_counterparty_by_id(counterparty_id)
    return result

@counterpartyRouter.put('/', response_model = CounterpartyOut)
async def update_counterparty(newCounterpartyIn : CounterpartyOut):
    result = await views.update_counterparty(newCounterpartyIn.dict())
    return result