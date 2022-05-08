from fastapi import APIRouter, Depends
from common_module.urls_module import qp_insert, qp_select_list, qp_select_one, qp_update, qp_select_one_by_iin
from documents.base_document.models import OptionsStructure
from references.document_type import views
from references.document_type.models import DocumentTypeOut, DocumentTypeIn
from typing import List, Union

document_typeRouter = APIRouter()


@document_typeRouter.get('/', response_model = Union[list[DocumentTypeOut],List[OptionsStructure]])
async def get_document_type_list(commons: dict = Depends(qp_select_list)):
    return await views.get_document_type_list(**commons)

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
