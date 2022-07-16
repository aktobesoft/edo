from fastapi import HTTPException
from sqlalchemy import select
from core.db import database

from catalogs.enum_types.models import EnumDocumentType

async def get_enum_document_type_id_by_metadata_name(metadata_name: str):
    query = select(EnumDocumentType.id).where(EnumDocumentType.metadata_name == metadata_name)
    result = await database.fetch_one(query)
    if result == None:
        raise HTTPException(status_code=404, detail="Item not found") 
    return result['id']

def enum_document_type_fillDataFromDict(queryResult : dict):
    return {
        'id': queryResult['enum_document_type_id'],
        'name': queryResult['enum_document_type_name'],
        'description': queryResult['enum_document_type_description']
        }
        
def business_type_fillDataFromDict(queryResult : dict):
    return {
        'id': queryResult['business_type_id'],
        'name': queryResult['business_type_name'],
        'full_name': queryResult['business_type_full_name'] 
        } 