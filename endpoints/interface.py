from typing import List
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, HTTPException, Request, Form
from sqlalchemy import select, insert, update
from core.db import database, engine, SessionLocal
from fastapi.templating import Jinja2Templates
from models.employee import Employee
from models.user import UserOut, User
from models.business_type import BusinessType
from models.entity import EntityOut, EntityNestedOut, Entity
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
                    BusinessType.full_name.label("type_full_name"), User.email.label("user_email"), User.name.label("user_name")).join(
                    BusinessType, Entity.type_id == BusinessType.id).join(User, Entity.user_id == User.id).order_by(Entity.id)
    records = await database.fetch_all(query)
    entity_list = []
    for rec in records:
        recordDict = dict(rec)
        entity_list.append(recordDict)
    return templates.TemplateResponse("entity/entity_list.html", context={'request': request, 'entityList': entity_list})

@interfaceRoute.get('/entity/new', response_class=HTMLResponse)
async def create_new_entity(request: Request):
    entity = Entity().asdict()
    entityLabel = Entity().get_html_attr()
    print(entity)
    print(entityLabel)
    return templates.TemplateResponse("entity/entity_detail.html", context={'request': request, 'entity': entity, 'entityLabel': entityLabel, 'is_new': True})

@interfaceRoute.post('/entity/new')
async def post_new_entity(request: Request):
    form_data = await request.form()
    entityInstance = dict(form_data)
    query = insert(Entity).values(name = entityInstance["name"], address = entityInstance["address"], comment = entityInstance["comment"],
                director = entityInstance["director"], director_phone = entityInstance["director_phone"], iin = entityInstance["iin"], 
                administrator = entityInstance["administrator"], administrator_phone = entityInstance["administrator_phone"], 
                startDate = datetime.strptime(entityInstance["startDate"], '%Y-%m-%d') if entityInstance["startDate"] != 'None' else datetime.now(), 
                endDate = datetime.strptime(entityInstance["endDate"], '%Y-%m-%d') if entityInstance["endDate"] != 'None' else datetime.now(), 
                type_id = int(entityInstance["type_id"]), user_id = int(entityInstance["user_id"]))
    newEntity = await database.fetch_one(query)
    response = RedirectResponse(status_code=HTTP_302_FOUND, url='/entity/')
    return response

@interfaceRoute.get("/entity/{entity_id}", response_class=HTMLResponse)
async def entity_detail(request: Request, entity_id: int):
    queryEntity = select(Entity).where(Entity.id == entity_id)
    resultEntity = await database.fetch_all(queryEntity)
    entityLabel = Entity().get_html_attr()
    if len(resultEntity) == 1:
        entity = dict(resultEntity[0])
        return templates.TemplateResponse("entity/entity_detail.html", context={'request': request, 'entity': entity, 'entityLabel': entityLabel, 'is_new': False})
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@interfaceRoute.post('/entity/{entity_id}')
async def post_entity(request: Request, entity_id: int):
    form_data = await request.form()
    entityInstance = dict(form_data)
    queryEntity = select(Entity).where(Entity.id == entity_id)
    resultEntity = await database.fetch_all(queryEntity)
    if len(resultEntity)>0:
        query = update(Entity).values(name = entityInstance["name"], address = entityInstance["address"], comment = entityInstance["comment"],
                    director = entityInstance["director"], director_phone = entityInstance["director_phone"], iin = entityInstance["iin"], 
                    administrator = entityInstance["administrator"], administrator_phone = entityInstance["administrator_phone"], 
                    startDate = datetime.strptime(entityInstance["startDate"], '%Y-%m-%d') if entityInstance["startDate"] != 'None' else datetime.now(), 
                    endDate = datetime.strptime(entityInstance["endDate"], '%Y-%m-%d') if entityInstance["endDate"] != 'None' else datetime.now(), 
                    type_id = int(entityInstance["type_id"]), user_id = int(entityInstance["user_id"])).where(Entity.id == entity_id)
        record = await database.fetch_all(query)
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
        