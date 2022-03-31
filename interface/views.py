from fastapi.responses import HTMLResponse
from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import select
from core.db import database, engine, SessionLocal
from fastapi.templating import Jinja2Templates
from models.references import Employee, Entity
from schemas.entity import EntityLabel

templates = Jinja2Templates(directory="templates")
interfaceRoute = APIRouter() 

@interfaceRoute.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("main_page.html", context={'request': request})

@interfaceRoute.get("/entity/", response_class=HTMLResponse)
async def entity_list(request: Request):
    query = select(Entity)
    records = await database.fetch_all(query)
    entity_list = []
    for rec in records:
        recordDict = dict(rec)
        #print(recordDict)
        entity_list.append(recordDict)
    #print(entity_list)
    return templates.TemplateResponse("entity/entity_list.html", context={'request': request, 'entityList': entity_list})

@interfaceRoute.get("/entity/{entity_id}", response_class=HTMLResponse)
async def entity_detail(request: Request, entity_id: int):
    query = select(Entity).where(Entity.id == entity_id)
    records = await database.fetch_all(query)
    entityLabel = EntityLabel()
    if len(records) == 1:
        entity = dict(records[0])
        return templates.TemplateResponse("entity/entity_detail.html", context={'request': request, 'entity': entity, 'entityLabel': entityLabel})
    else:
        raise HTTPException(status_code=404, detail="Item not found")