import email
from typing import List, Optional
from fastapi import APIRouter, Depends
from models.entity import Entity, EntityIn, EntityOptionsOut, EntityOut
from models.employee import Employee, EmployeeIn, EmployeeOut
from services import entity as entityService, user as userService, employee as employeeService
from models.business_type import BusinessTypeOut, BusinessTypeOptionsOut, BusinessType
from models.user import UserIn, UserOptionsOut, UserOut, User
from models.notes import NotesOut, Notes
from core.db import database
from sqlalchemy import select, insert, tuple_, join

async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

apiRouter = APIRouter()

@apiRouter.get('/business_type/', response_model = List[BusinessTypeOut])
async def get_business_type_list(commons: dict = Depends(common_parameters)):
    query = select(BusinessType.id, BusinessType.name, BusinessType.full_name)
    records = await database.fetch_all(query)
    listValue = []
    
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

@apiRouter.get('/business_type_options/', response_model = List[BusinessTypeOptionsOut])
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

@apiRouter.get('/user_options/', response_model = List[UserOptionsOut])
async def get_user_options_list(commons: dict = Depends(common_parameters)):
    listValue = await userService.get_user_options_list(**commons)
    return listValue

@apiRouter.get('/user/', response_model = List[UserOut])
async def get_user_list(commons: dict = Depends(common_parameters)):
    listValue = await userService.get_user_list(**commons)
    return listValue

# ----------------------------------------------
# +++ ---------------- entity ------------------
@apiRouter.get('/entity/', response_model=list[EntityOut])
async def get_entity_list(commons: dict = Depends(common_parameters)):
    return await entityService.get_entity_list(**commons)

@apiRouter.get('/entity/{entity_id}', response_model=EntityOut)
async def get_entity_by_id(entity_id: int):
    return await entityService.get_entity_by_id(entity_id)

@apiRouter.post('/entity/', response_model = EntityOut)
async def post_entity(newEntityIn : EntityIn):
    newEntity = await entityService.post_entity(newEntityIn)
    return newEntity

@apiRouter.delete('/entity/{entity_id}')
async def post_entity(entity_id : int):
    newEntity = await entityService.delete_entity_by_id(entity_id)
    return newEntity

@apiRouter.put('/entity/', response_model = EntityOut)
async def update_entity(newEntityIn : EntityOut):
    newEntityIn = dict(newEntityIn)
    newEntity = await entityService.update_entity(newEntityIn['id'], newEntityIn)
    newEntity = await entityService.get_entity_by_id(newEntityIn['id'])
    return newEntity

@apiRouter.get('/entity_options/', response_model = List[EntityOptionsOut])
async def get_entity_options_list(commons: dict = Depends(common_parameters)):
    listValue = await entityService.get_entity_options_list(**commons)
    return listValue
# +++ ---------------- entity ------------------
# ----------------------------------------------

# ----------------------------------------------
# +++ ---------------- employee ------------------
@apiRouter.get('/employee/', response_model=list[EmployeeOut])
async def get_employee_list(commons: dict = Depends(common_parameters)):
    return await employeeService.get_employee_list(**commons)

@apiRouter.get('/employee/{employee_id}', response_model=EmployeeOut)
async def get_employee_by_id(employee_id: int):
    return await employeeService.get_employee_by_id(employee_id)

@apiRouter.post('/employee/', response_model = EmployeeOut)
async def post_employee(newEmployeeIn : EmployeeIn):
    newEmployee = await employeeService.post_employee(newEmployeeIn)
    return newEmployee

@apiRouter.delete('/employee/{employee_id}')
async def post_employee(employee_id : int):
    newEmployee = await employeeService.delete_employee_by_id(employee_id)
    return newEmployee

@apiRouter.put('/employee/', response_model = EmployeeOut)
async def update_employee(newEmployeeIn : EmployeeOut):
    newEmployeeIn = dict(newEmployeeIn)
    newEmployee = await employeeService.update_employee(newEmployeeIn['id'], newEmployeeIn)
    newEmployee = await employeeService.get_employee_by_id(newEmployeeIn['id'])
    return newEmployee
# +++ ---------------- employee ------------------
# ----------------------------------------------

# ---------------- user ------------------
@apiRouter.post('/user/', response_model = UserOut)
async def post_user(newUser : UserIn):
    newUser = await userService.post_user(newUser)
    return dict(newUser)
     
# ---------------- notes ------------------
@apiRouter.get("/notes", response_model=List[NotesOut])
async def read_notes(commons: dict = Depends(common_parameters)):
    list1 = [tuple_(50, True),tuple_(51, True)]
    query = select(Notes.id, Notes.text, Notes.completed).where(tuple_(Notes.id, Notes.completed).in_(list1))
    listValue = await database.fetch_all(query)
    return listValue