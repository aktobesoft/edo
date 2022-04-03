from typing import List
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, HTTPException, Request, Form
from sqlalchemy import select, insert, update
from core.db import database, engine, SessionLocal
from fastapi.templating import Jinja2Templates
from models.references import Employee, Entity, User, BusinessType
from schemas.references import EntityLabel, EntityOut, EntityNestedOut
from datetime import datetime
from starlette.status import HTTP_302_FOUND

templates = Jinja2Templates(directory="templates")
interfaceRoute = APIRouter() 

@interfaceRoute.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("main_page.html", context={'request': request})

@interfaceRoute.get("/entity/", response_class=HTMLResponse)
async def entity_list(request: Request):
    query = select(Entity.id, Entity.iin, Entity.name, Entity.startDate, Entity.endDate, BusinessType.name.label("type"), 
                    BusinessType.full_name.label("type_full_name"), User.email.label("user")).join(
                    BusinessType, Entity.type_id == BusinessType.id).join(User, Entity.user_id == User.id).order_by(Entity.id)
    records = await database.fetch_all(query)
    entity_list = []
    for rec in records:
        recordDict = dict(rec)
        #print(recordDict)
        entity_list.append(recordDict)
    #print(entity_list)
    return templates.TemplateResponse("entity/entity_list.html", context={'request': request, 'entityList': entity_list})

""" @interfaceRoute.get("/entity/{entity_id}", response_class=HTMLResponse)
async def entity_detail(request: Request, entity_id: int):
    queryEntity = select(Entity).where(Entity.id == entity_id)
    resultEntity = await database.fetch_all(queryEntity)
    entityLabel = EntityLabel()
    if len(resultEntity) == 1:
        entity = dict(resultEntity[0])
        quertUser = select(User).where(User.is_active)
        resultUser = await database.fetch_all(quertUser)
        userList = []
        for resultItem in resultUser:
            user = dict(resultItem)
            userList.append({'id': user['id'], 
                            'email': user['email'], 
                            'selected': True if user['id'] == entity['user_id'] else False
                            })
        entity['user_id'] = userList
        return templates.TemplateResponse("entity/entity_detail.html", context={'request': request, 'entity': entity, 'entityLabel': entityLabel})
    else:
        raise HTTPException(status_code=404, detail="Item not found") """

@interfaceRoute.get("/entity/{entity_id}", response_class=HTMLResponse)
async def entity_detail(request: Request, entity_id: int):
    queryEntity = select(Entity).where(Entity.id == entity_id)
    resultEntity = await database.fetch_all(queryEntity)
    entityLabel = EntityLabel()
    if len(resultEntity) == 1:
        entity = dict(resultEntity[0])
        # quertUser = select(User).where(User.is_active)
        # resultUser = await database.fetch_all(quertUser)
        # userList = []
        # for resultItem in resultUser:
        #     user = dict(resultItem)
        #     userList.append({'id': user['id'], 
        #                     'email': user['email'], 
        #                     'selected': True if user['id'] == entity['user_id'] else False
        #                     })
        #entity['user_id'] = userList
        return templates.TemplateResponse("entity/entity_detail.html", context={'request': request, 'entity': entity, 'entityLabel': entityLabel})
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@interfaceRoute.post('/entity/{entity_id}')
#@apiRouter.post('/entity/'), response_model = HTMLResponse
async def post_entity(request: Request, entity_id: int):
    form_data = await request.form()
    entityInstance = dict(form_data)
    print(entityInstance)
    queryEntity = select(Entity).where(Entity.id == entity_id)
    resultEntity = await database.fetch_all(queryEntity)
    print(entityInstance["startDate"])
    if len(resultEntity)>0:
        query = update(Entity).values(name = entityInstance["name"], address = entityInstance["address"], comment = entityInstance["comment"],
                    director = entityInstance["director"], director_phone = entityInstance["director_phone"], iin = entityInstance["iin"], 
                    administrator = entityInstance["administrator"], administrator_phone = entityInstance["administrator_phone"], 
                    startDate = datetime.strptime(entityInstance["startDate"], '%Y-%m-%d') if entityInstance["startDate"] != 'None' else datetime.now(), 
                    endDate = datetime.strptime(entityInstance["endDate"], '%Y-%m-%d') if entityInstance["endDate"] != 'None' else datetime.now(), 
                    type_id = int(entityInstance["type_id"]), user_id = int(entityInstance["user_id"])).where(Entity.id == entity_id)
        record = await database.fetch_all(query)
        for rec in record:
            print(dict(rec))
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
    response = RedirectResponse(status_code=HTTP_302_FOUND, url='/entity/')
    return response

@interfaceRoute.get("/entity2/", response_model = EntityNestedOut)
def entity_list(request: Request):
    query = select(Entity).where(Entity.id == 5)
    session = SessionLocal()
    records = session.execute(query) 
    k = records.first()[0]
    return k

@interfaceRoute.get("/entity2/{entity_id}", response_class=HTMLResponse)
async def entity_detail(request: Request, entity_id: int):
    queryEntity = select(Entity).where(Entity.id == entity_id)
    session = SessionLocal()
    records = session.execute(queryEntity)
    if records == None: 
        raise HTTPException(status_code=404, detail="Item not found")
    entityLabel = EntityLabel()
    entity = records.first()[0]
    return templates.TemplateResponse("entity/entity_detail2.html", context={'request': request, 'entity': entity, 'entityLabel': entityLabel})
        