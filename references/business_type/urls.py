from fastapi import APIRouter, Depends
from common_module.urls_module import common_parameters
from typing import List

from references.business_type.models import BusinessTypeOut, BusinessTypeOptionsOut, BusinessTypeIn
from references.business_type import views


business_typeRouter = APIRouter()

@business_typeRouter.get('/options/', response_model = List[BusinessTypeOptionsOut])
async def get_business_type_options_list(commons: dict = Depends(common_parameters)):
    records = await views.get_business_type_options_list(**commons)
    return records

@business_typeRouter.get('/', response_model = List[BusinessTypeOut])
async def get_business_type_list(commons: dict = Depends(common_parameters)):
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
