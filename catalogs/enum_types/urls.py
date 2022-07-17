from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, get_current_active_user
from common_module.urls_module import paginator_execute, query_parameters_list
from typing import List, Union

from catalogs.enum_types.models import EnumBusinessTypeOut, EnumDocumentTypeOut
import catalogs.enum_types.views as views
from documents.base_document.models import OptionsStructure, OptionsStructureStr


enum_typeRouter = APIRouter()

@enum_typeRouter.get('/business_type_list', response_model = Union[List[EnumBusinessTypeOut], List[OptionsStructureStr]])
async def get_enum_business_type_list(parameters: dict = Depends(query_parameters_list), current_user: UserModel = Depends(get_current_active_user)):
    records = await views.get_enum_business_type_list(**parameters)
    return records

@enum_typeRouter.get('/document_type_list', response_model = List[EnumDocumentTypeOut])
async def get_enum_document_type_list(parameters: dict = Depends(query_parameters_list), current_user: UserModel = Depends(get_current_active_user)):
    records =  await views.get_enum_document_type_list(**parameters)
    return records