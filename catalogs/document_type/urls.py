from fastapi import APIRouter, Depends
from common_module.urls_module import paginator_execute, qp_insert, qp_select_list, qp_select_one, qp_update
from documents.base_document.models import OptionsStructure
from catalogs.document_type import views
from catalogs.document_type.models import DocumentTypeListOut, DocumentTypeOut, DocumentTypeIn
from typing import List, Union

document_typeRouter = APIRouter()


@document_typeRouter.get('/', response_model = DocumentTypeListOut)
async def get_document_type_list(query_param: dict = Depends(qp_select_list)):
    parametrs = await paginator_execute(query_param, await views.get_document_type_count())
    return {'info': parametrs, 'result': await views.get_document_type_list(**parametrs)}

@document_typeRouter.get('/{document_type_iin}', response_model=DocumentTypeOut)
async def get_document_type_by_iin(document_type_iin: str, qp_select_one: dict = Depends(qp_select_one)):
    return await views.get_document_type_by_iin(document_type_iin)

@document_typeRouter.post('/', response_model = DocumentTypeOut)
async def post_document_type(document_typeInstance : DocumentTypeIn):#, qp_insert: dict = Depends(qp_insert)):
    document_typeDict = document_typeInstance.dict()
    result = await views.post_document_type(document_typeDict)
    return result

@document_typeRouter.delete('/{document_type_iin}')
async def post_document_type(document_type_iin: str):
    result = await views.delete_document_type_by_iin(document_type_iin)
    return result

@document_typeRouter.put('/{document_type_id}', response_model = DocumentTypeOut)
async def update_document_type(document_type_id: int, newDocumentTypeIn : DocumentTypeOut):#, qp_update: dict = Depends(qp_update)):
    newDocumentTypeIn = dict(newDocumentTypeIn)
    result = await views.update_document_type(newDocumentTypeIn, document_type_id)
    return newDocumentTypeIn