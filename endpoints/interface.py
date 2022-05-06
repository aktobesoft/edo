from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, HTTPException, Request, Form
from common_module.urls_module import qp_select_one
from fastapi.templating import Jinja2Templates
from references.counterparty.models import Counterparty
from references.employee.models import Employee
from references.employee import views as employeeService
from references.entity import views as entityService
from references.counterparty import views as counterpartyService
from references.approval_template.views import get_approval_template_by_id, get_approval_template_list
from references.entity.models import Entity
from datetime import datetime
from starlette.status import HTTP_302_FOUND

from references.enum_types.models import step_type

templates = Jinja2Templates(directory="templates")
interfaceRoute = APIRouter() 

@interfaceRoute.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("main_page.html", context={'request': request})

# ----------------------------------------------
# +++ ---------------- entity ------------------
@interfaceRoute.get("/entity/", response_class=HTMLResponse)
async def entity_list(request: Request):
    commons = {'limit': 100, 'skip': 0, 'nested': True}
    entity_list = await entityService.get_entity_list(**commons)
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

@interfaceRoute.get('/entity/{entity_iin}/delete')
async def delete_entity(request: Request, entity_iin: str):
    newEntity = await entityService.delete_entity_by_iin(entity_iin)
    response = RedirectResponse(status_code=HTTP_302_FOUND, url='/entity/')
    return response

@interfaceRoute.get("/entity/{entity_iin}", response_class=HTMLResponse)
async def entity_detail(request: Request, entity_iin: str):
    resultEntity = await entityService.get_entity_by_iin(entity_iin)
    if resultEntity != None:
        entity = dict(resultEntity)
        entityLabel = Entity().get_html_attr()
        return templates.TemplateResponse("entity/entity_detail.html", context={'request': request, 'entity': entity, 'entityLabel': entityLabel, 'is_new': False})
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@interfaceRoute.post('/entity/{entity_iin}')
async def update_entity(request: Request, entity_iin: str):
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
    commons = {'limit': 100, 'skip': 0, 'nested': True}
    employee_list = await employeeService.get_employee_list(**commons)
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

# ----------------------------------------------
# +++ ---------------- counterparty ------------------
@interfaceRoute.get("/counterparty/", response_class=HTMLResponse)
async def counterparty_list(request: Request):
    parametrs = {'limit': 100, 'skip': 0, 'nested': True}
    counterparty_list = await counterpartyService.get_counterparty_nested_list(**parametrs)
    return templates.TemplateResponse("counterparty/counterparty_list.html", context={'request': request, 'counterpartyList': counterparty_list})

@interfaceRoute.get("/counterparty/{itemId}", response_class=HTMLResponse)
async def counterparty_detail(request: Request, itemId: str):
    
    if itemId == 'new':
        resultDict = {}
        objectLabel = Counterparty().get_html_attr()
        return templates.TemplateResponse("counterparty/counterparty_detail.html", context={'request': request, 'counterparty': resultDict, 'counterpartyLabel': objectLabel, 'is_new': True})
    
    _qp_select_one = await qp_select_one()
    result = await counterpartyService.get_counterparty_by_iin(itemId, **_qp_select_one)
    if result != None:
        resultDict = dict(result)
        objectLabel = Counterparty().get_html_attr()
        return templates.TemplateResponse("counterparty/counterparty_detail.html", context={'request': request, 'counterparty': resultDict, 'counterpartyLabel': objectLabel, 'is_new': False})
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@interfaceRoute.post('/counterparty/{itemId}')
async def update_counterparty(request: Request, itemId: str):
    form_data = await request.form()
    counterpartyInstance = dict(form_data)
    if itemId == 'new':
        result = await counterpartyService.post_counterparty(counterpartyInstance)
    else:
        result = await counterpartyService.update_counterparty(counterpartyInstance)
    return RedirectResponse(status_code=HTTP_302_FOUND, url='/counterparty/')

@interfaceRoute.get('/counterparty/{itemId}/delete')
async def delete_employee(request: Request, itemId: str):
    result = await counterpartyService.delete_counterparty_by_iin(itemId)
    response = RedirectResponse(status_code=HTTP_302_FOUND, url='/counterparty/')
    return response
# +++ ---------------- counterparty ------------------
# ----------------------------------------------

@interfaceRoute.get("/approval_template/", response_class=HTMLResponse)
async def approval_template_list(request: Request):
    listOfValue = await get_approval_template_list(nested = True) 
    return templates.TemplateResponse("approval_template/approval_template_list.html", context={'request': request, 'listOfValue': listOfValue})

@interfaceRoute.get("/approval_template/{itemId}", response_class=HTMLResponse)
async def approval_template_detail(request: Request, itemId: int):
    parametrs = {'nested': True}
    approval_template = await get_approval_template_by_id(itemId, **parametrs)
    # _approval_template = dict(approval_template)
    for item in approval_template['steps']:
        item['type'] = 'Линейное' if item['type'] == step_type.line  else 'Паралельное'
    # _approval_template['type'] = 'Линейное' if _approval_template['type'] == step_type.line else 'Паралельное'
    return templates.TemplateResponse("approval_template/approval_template_detail.html", context={'request': request, 'approval_template': approval_template, 'itemId': itemId})