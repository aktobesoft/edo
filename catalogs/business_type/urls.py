from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, get_current_active_user
from common_module.urls_module import query_parameters_list
from typing import List, Union

from catalogs.business_type.models import BusinessTypeOut, BusinessTypeIn
from catalogs.business_type import views
from documents.base_document.models import OptionsStructure, OptionsStructureStr


business_typeRouter = APIRouter()

@business_typeRouter.get('/', response_model = Union[List[BusinessTypeOut], List[OptionsStructureStr]])
async def get_business_type_list(parameters: dict = Depends(query_parameters_list), current_user: UserModel = Depends(get_current_active_user)):
    records = await views.get_business_type_list(**parameters)
    return records

@business_typeRouter.get('/{business_type_id}')
async def get_business_type_by_id(business_type_id : int, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.get_business_type_by_id(business_type_id)
    return result

@business_typeRouter.post('/', response_model = BusinessTypeOut)
async def post_business_type(business_typeInstance : BusinessTypeIn, current_user: UserModel = Depends(get_current_active_user)):
    businessTypeDict = business_typeInstance.dict()
    result = await views.post_business_type(businessTypeDict)
    return result

@business_typeRouter.put('/', response_model = BusinessTypeOut)
async def update_business_type(newBusinessTypeIn : BusinessTypeOut, current_user: UserModel = Depends(get_current_active_user)):
    newBusinessTypeIn = dict(newBusinessTypeIn)
    result = await views.update_business_type(newBusinessTypeIn)
    return newBusinessTypeIn

@business_typeRouter.delete('/{business_type_id}')
async def delete_business_type_by_id(business_type_id : int, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.delete_business_type_by_id(business_type_id)
    return result
