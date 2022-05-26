from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, get_current_active_user
from common_module.urls_module import paginator_execute, qp_select_list, qp_select_one
import catalogs.counterparty.views as views
from documents.base_document.models import OptionsStructure
from catalogs.counterparty.models import CounterpartyListNestedOut, CounterpartyListOut, CounterpartyOut, CounterpartyIn, CounterpartyNestedOut
from typing import List, Union

counterpartyRouter = APIRouter()

@counterpartyRouter.get('/', response_model=Union[CounterpartyListNestedOut,CounterpartyListOut])
async def get_counterparty_list(query_param: dict = Depends(qp_select_list), current_user: UserModel = Depends(get_current_active_user)):
    parametrs = await paginator_execute(query_param, await views.get_employee_count())
    return {'info': parametrs, 'result': await views.get_counterparty_list(**parametrs)}

@counterpartyRouter.get('/{counterparty_iin}', response_model=Union[CounterpartyNestedOut, CounterpartyOut])
async def get_counterparty_by_iin(counterparty_iin: str, qp_select_one: dict = Depends(qp_select_one), current_user: UserModel = Depends(get_current_active_user)):
    return await views.get_counterparty_by_iin(counterparty_iin,**qp_select_one)

@counterpartyRouter.post('/', response_model = CounterpartyOut)
async def post_counterparty(newCounterpartyIn : CounterpartyIn, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.post_counterparty(newCounterpartyIn.dict())
    return result

@counterpartyRouter.delete('/{counterparty_iin}')
async def delete_counterparty_by_iin(counterparty_iin: str, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.delete_counterparty_by_iin(counterparty_iin)
    return result

@counterpartyRouter.put('/{counterparty_iin}', response_model = CounterpartyOut)
async def update_counterparty(counterparty_iin: str, newCounterpartyIn : CounterpartyOut, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.update_counterparty(newCounterpartyIn.dict(), counterparty_iin)
    return result