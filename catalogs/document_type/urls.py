from fastapi import APIRouter, Depends
from auth.user_auth import UserModel, get_current_active_user
from common_module.urls_module import paginator_execute, query_parameters_list, query_parameters
from documents.base_document.models import OptionsStructure
import catalogs.document_type.views as views
from catalogs.document_type.models import DocumentTypeListOut, DocumentTypeOut, DocumentTypeIn
from typing import List, Union

document_typeRouter = APIRouter()


@document_typeRouter.get('/', response_model = DocumentTypeListOut)
async def get_document_type_list(parameters: dict = Depends(query_parameters_list), current_user: UserModel = Depends(get_current_active_user)):
    await paginator_execute(parameters, await views.get_document_type_count())
    return {'info': parameters, 'result': await views.get_document_type_list(**parameters)}

@document_typeRouter.get('/{document_type_iin}', response_model=DocumentTypeOut)
async def get_document_type_by_iin(document_type_iin: str, parameters: dict = Depends(query_parameters), current_user: UserModel = Depends(get_current_active_user)):
    return await views.get_document_type_by_iin(document_type_iin)

@document_typeRouter.post('/', response_model = DocumentTypeOut)
async def post_document_type(document_typeInstance : DocumentTypeIn, current_user: UserModel = Depends(get_current_active_user)):
    document_typeDict = document_typeInstance.dict()
    result = await views.post_document_type(document_typeDict)
    return result

@document_typeRouter.delete('/{document_type_iin}')
async def post_document_type(document_type_iin: str, current_user: UserModel = Depends(get_current_active_user)):
    result = await views.delete_document_type_by_iin(document_type_iin)
    return result

@document_typeRouter.put('/{document_type_id}', response_model = DocumentTypeOut)
async def update_document_type(document_type_id: int, newDocumentTypeIn : DocumentTypeOut, current_user: UserModel = Depends(get_current_active_user)):
    newDocumentTypeIn = dict(newDocumentTypeIn)
    result = await views.update_document_type(newDocumentTypeIn, document_type_id)
    return newDocumentTypeIn
