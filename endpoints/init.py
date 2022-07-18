import email
from importlib.metadata import metadata
from typing import List
from unicodedata import name
from fastapi import APIRouter
from catalogs.counterparty.models import Counterparty, CounterpartyOut
from catalogs.entity.models import Entity, EntityNestedOut
from catalogs.enum_types.models import EnumBusinessType
from catalogs.enum_types.models import EnumDocumentType
from catalogs.enum_types.models import EnumTaskStatusType, EnumProcessStatusType, EnumRouteStatusType, EnumStepType
from catalogs.user.models import User
from core.db import database, SessionLocal
from sqlalchemy import select, insert, tuple_, join

initRouter = APIRouter()
session = SessionLocal()

@initRouter.get('/createEnumBusinessType')
def create_Enum_Business_Type():
    typeList = []
    typeList.append(EnumBusinessType(name = 'АО', full_name = 'Акционерное Общество'))
    typeList.append(EnumBusinessType(name = 'ТОО', full_name = 'Товарищество с ограниченной ответственностью'))
    typeList.append(EnumBusinessType(name = 'ИП', full_name = 'Индивидуальный предприниматель'))
    typeList.append(EnumBusinessType(name = 'ФизЛицо', full_name = 'Физическое лицо'))
    typeList.append(EnumBusinessType(name = 'ГП', full_name = 'Государственное предприятие'))
    session.add_all(typeList)
    try:
        session.commit()
        return {'status': 'done'}
    except:
        return {'status': 'error'}

@initRouter.get('/createProcessStatusType')
async def create_Process_Status_Type():

    typeList = []
    typeList.append(EnumProcessStatusType(name = 'подписан', description = 'Подписан'))
    typeList.append(EnumProcessStatusType(name = 'отклонен', description = 'Отклонен'))
    typeList.append(EnumProcessStatusType(name = 'отменен', description = 'Отменен'))
    typeList.append(EnumProcessStatusType(name = 'в работе', description = 'В работе'))
    typeList.append(EnumProcessStatusType(name = 'черновик', description = 'Черновик'))
    session.add_all(typeList)
    try:
        session.commit()
        return {'status': 'done'}
    except:
        return {'status': 'error'}

@initRouter.get('/createApproveStepType')
def create_Approve_Step_Type():
    typeList = []

    typeList.append(EnumStepType(name = 'линейное', description = 'Линейное'))
    typeList.append(EnumStepType(name = 'параллельное', description = 'Параллельное'))

    session.add_all(typeList)
    try:
        session.commit()
        return {'status': 'done'}
    except:
        return {'status': 'error'}

@initRouter.get('/createRouteStatusType')
def create_Route_Status_Type():
    typeList = []

    typeList.append(EnumRouteStatusType(name = 'согласован', description = 'Согласован'))
    typeList.append(EnumRouteStatusType(name = 'отклонен', description = 'Отклонен'))

    session.add_all(typeList)
    try:
        session.commit()
        return {'status': 'done'}
    except:
        return {'status': 'error'}

@initRouter.get('/createTaskStatusType')
def create_Task_Status_Type():
    typeList = []

    # 'в работе', 'выполнено', 'отложено', 'в ожидании', 'не выполнено', 'переназначено', 'новый'
    typeList.append(EnumTaskStatusType(name = 'в работе', description = 'В работе'))
    typeList.append(EnumTaskStatusType(name = 'выполнено', description = 'Выполнено'))
    typeList.append(EnumTaskStatusType(name = 'отложено', description = 'Отложено'))
    typeList.append(EnumTaskStatusType(name = 'в ожидании', description = 'В ожидании'))
    typeList.append(EnumTaskStatusType(name = 'не выполнено', description = 'Не выполнено'))
    typeList.append(EnumTaskStatusType(name = 'переназначено', description = 'Переназначено'))
    typeList.append(EnumTaskStatusType(name = 'новый', description = 'Новый'))

    session.add_all(typeList)
    try:
        session.commit()
        return {'status': 'done'}
    except:
        return {'status': 'error'}

@initRouter.get('/get_entityList',response_model=List[EntityNestedOut])
def get_entity_List():
    query = select(Entity)
    session = SessionLocal()
    result = session.execute(query)
    resultAll = result.scalars().all()
    return resultAll

@initRouter.get('/getCounterpartyList',response_model=List[CounterpartyOut])
def get_Counterparty_List():
    query = select(Counterparty)
    session = SessionLocal()
    result = session.execute(query)
    resultAll = result.scalars().all()
    return resultAll

# @initRouter.get('/createCounterpartyList')
# def get_entityList():
#     f = open("demofile.txt", "r")
#     for x in f:
#         print(x)
#     query = select(Entity)
#     session = SessionLocal()
#     result = session.execute(query)
#     resultAll = result.scalars().all()
#     return resultAll


@initRouter.get('/createAdmin')
def create_Admin_User():
    typeList = []
    typeList.append(User(name = 'Admin', email = 'admin@email.com', is_active = True, is_company = False))
    session.add_all(typeList)
    session.commit()
    return {'status': 'done'}

@initRouter.get('/createEnumDocumentType')
def create_Enum_Document_Type():
    typeList = []
    typeList.append(EnumDocumentType(name = "ЗаявкаНаРасходованиеДенежныхСредств", description = "Заявка на расходование денежных средств", metadata_name = "purchase_requisition"))
    typeList.append(EnumDocumentType(name = "СлужебнаяЗапискаНаИсполнение", description = "Служебная записка на исполнение", metadata_name = "employee_task"))

    session.add_all(typeList)
    try:
        session.commit()
        return {'status': 'done'}
    except:
        return {'status': 'error'}