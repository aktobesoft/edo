from fastapi import APIRouter, Depends
from common_module.urls_module import qp_select_list
from typing import List, Union

from references.business_type.models import BusinessTypeOut, BusinessTypeIn
from references.business_type import views
from documents.base_document.models import OptionsStructure


business_typeRouter = APIRouter()

@business_typeRouter.get('/', response_model = Union[List[BusinessTypeOut], List[OptionsStructure]])
async def get_business_type_list(commons: dict = Depends(qp_select_list)):
    records = await views.get_business_type_list(**commons)
    return records

@business_typeRouter.get('/{business_type_id}')
async def get_business_type_by_id(business_type_id : int):
    result = await views.get_business_type_by_id(business_type_id)
    return result

@business_typeRouter.post('/', response_model = BusinessTypeOut)
async def post_business_type(business_typeInstance : BusinessTypeIn):
    businessTypeDict = business_typeInstance.dict()
    result = await views.post_business_type(businessTypeDict)
    return result

@business_typeRouter.put('/', response_model = BusinessTypeOut)
async def update_business_type(newBusinessTypeIn : BusinessTypeOut):
    newBusinessTypeIn = dict(newBusinessTypeIn)
    result = await views.update_business_type(newBusinessTypeIn)
    return newBusinessTypeIn

@business_typeRouter.delete('/{business_type_id}')
async def delete_business_type_by_id(business_type_id : int):
    result = await views.delete_business_type_by_id(business_type_id)
    return result
