from operator import mod
from fastapi import APIRouter, Depends
from common_module.urls_module import common_parameters
from core.db import database
from sqlalchemy import select
from typing import List

from references.employee.models import EmployeeOut, EmployeeIn
from references.business_type.models import BusinessType, BusinessTypeOut, BusinessTypeOptionsOut


business_typeRouter = APIRouter()

@business_typeRouter.get('/', response_model = List[BusinessTypeOut])
async def get_business_type_list(commons: dict = Depends(common_parameters)):
    query = select(BusinessType.id, BusinessType.name, BusinessType.full_name)
    records = await database.fetch_all(query)
    listValue = []
    
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

@business_typeRouter.get('/options/', response_model = List[BusinessTypeOptionsOut])
async def get_business_type_options_list(commons: dict = Depends(common_parameters)):
    query = select(BusinessType.id, BusinessType.name, BusinessType.full_name)
    records = await database.fetch_all(query)
    listValue = []
    
    for rec in records:
        recordDict = dict(rec)
        recordDictOption = {}
        recordDictOption['text'] =  recordDict['full_name']
        recordDictOption['value'] =  recordDict['id'] 
        listValue.append(recordDictOption) 
    return listValue