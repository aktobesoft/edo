from typing import List
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, HTTPException, Request, Form
from sqlalchemy import select, insert, update
from core.db import database, engine, SessionLocal
from fastapi.templating import Jinja2Templates
from references.employee.models import Employee
from references.user.models import UserOut, User
from references.employee import views as employeeService
from references.entity import views as entityService
from references.user import views as userService
from references.business_type.models import BusinessType
from references.entity.models import EntityOut, EntityNestedOut, Entity
from datetime import datetime
from starlette.status import HTTP_302_FOUND

templates = Jinja2Templates(directory="templates")
interfaceRoute = APIRouter() 

@interfaceRoute.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("main_page.html", context={'request': request})

# ----------------------------------------------
# +++ ---------------- entity ------------------
@interfaceRoute.get("/entity/", response_class=HTMLResponse)
async def entity_list(request: Request):
    commons = {'limit': 100, 'skip': 0}
    entity_list = await entityService.get_entity_list(**commons, addUser = True, addBusinessType = True)
    return templates.TemplateResponse("entity/entity_list.html", context={'request': request, 'entityList': entity_list})

@interfaceRoute.get('/entity/new', response_class=HTMLResponse)
async def create_new_entity(request: Request):
    entity = Entity().asdict()
    entityLabel = Entity().get_html_attr()
    return templates.TemplateResponse("entity/entity_detail.html", context={'request': request, 'entity': entity, 'entityLabel': entityLabel, 'is_new': True})

@interfaceRoute.post('/entity/new')
async def post_new_entity(request: Request):
    form_data = await request.form()
    entityInstance = dict(form_data)
    newEntity = await entityService.post_entity(entityInstance)
    response = RedirectResponse(status_code=HTTP_302_FOUND, url='/entity/')
    return response

@interfaceRoute.get('/entity/{entity_id}/delete')
async def delete_entity(request: Request, entity_id: int):
    newEntity = await entityService.delete_entity_by_id(entity_id)
    response = RedirectResponse(status_code=HTTP_302_FOUND, url='/entity/')
    return response

@interfaceRoute.get("/entity/{entity_id}", response_class=HTMLResponse)
async def entity_detail(request: Request, entity_id: int):
    resultEntity = await entityService.get_entity_by_id(entity_id)
    if resultEntity != None:
        entity = dict(resultEntity)
        entityLabel = Entity().get_html_attr()
        return templates.TemplateResponse("entity/entity_detail.html", context={'request': request, 'entity': entity, 'entityLabel': entityLabel, 'is_new': False})
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@interfaceRoute.post('/entity/{entity_id}')
async def update_entity(request: Request, entity_id: int):
    form_data = await request.form()
    entityInstance = dict(form_data)
    resultEntity = await entityService.update_entity(entityInstance)
    return RedirectResponse(status_code=HTTP_302_FOUND, url='/entity/')
# +++ ---------------- entity ------------------
# ----------------------------------------------

# ----------------------------------------------
# +++ ---------------- employee ------------------
@interfaceRoute.get("/employee/", response_class=HTMLResponse)
async def employee_list(request: Request):
    commons = {'limit': 100, 'skip': 0}
    employee_list = await employeeService.get_employee_list(**commons, addUser = True, addBusinessType = True)
    return templates.TemplateResponse("employee/employee_list.html", context={'request': request, 'employeeList': employee_list})

@interfaceRoute.get('/employee/new', response_class=HTMLResponse)
async def create_new_employee(request: Request):
    employee = Employee().asdict()
    employeeLabel = Employee().get_html_attr()
    return templates.TemplateResponse("employee/employee_detail.html", context={'request': request, 'employee': employee, 'employeeLabel': employeeLabel, 'is_new': True})

@interfaceRoute.post('/employee/new')
async def post_new_employee(request: Request):
    form_data = await request.form()
    employeeInstance = dict(form_data)
    newEmployee = await employeeService.post_employee(employeeInstance)
    response = RedirectResponse(status_code=HTTP_302_FOUND, url='/employee/')
    return response

@interfaceRoute.get('/employee/{employee_id}/delete')
async def delete_employee(request: Request, employee_id: int):
    newEmployee = await employeeService.delete_employee_by_id(employee_id)
    response = RedirectResponse(status_code=HTTP_302_FOUND, url='/employee/')
    return response

@interfaceRoute.get("/employee/{employee_id}", response_class=HTMLResponse)
async def employee_detail(request: Request, employee_id: int):
    resultEmployee = await employeeService.get_employee_by_id(employee_id)
    if resultEmployee != None:
        employee = dict(resultEmployee)
        employeeLabel = Employee().get_html_attr()
        return templates.TemplateResponse("employee/employee_detail.html", context={'request': request, 'employee': employee, 'employeeLabel': employeeLabel, 'is_new': False})
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@interfaceRoute.post('/employee/{employee_id}')
async def update_employee(request: Request, employee_id: int):
    form_data = await request.form()
    employeeInstance = dict(form_data)
    resultEmployee = await employeeService.update_employee(employeeInstance)
    return RedirectResponse(status_code=HTTP_302_FOUND, url='/employee/')
# +++ ---------------- employee ------------------
# ----------------------------------------------
