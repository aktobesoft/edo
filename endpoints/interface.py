from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from common_module.urls_module import paginator, paginator_execute, qp_select_list, qp_select_one
from fastapi.templating import Jinja2Templates
from documents.purchase_requisition.views import get_purchase_requisition_by_id, get_purchase_requisition_list
from catalogs.approval_process.urls import get_approval_process_list
from catalogs.approval_template.models import ApprovalTemplate
from catalogs.counterparty.models import Counterparty
from catalogs.employee.models import Employee
from catalogs.employee import views as employeeService
from catalogs.entity import views as entityService
from catalogs.counterparty import views as counterpartyService
from catalogs.approval_template.views import get_approval_template_by_id, get_approval_template_list
from catalogs.entity.models import Entity
from datetime import datetime
from starlette.status import HTTP_302_FOUND

from catalogs.enum_types.models import StepType

templates = Jinja2Templates(directory="templates")
interfaceRoute = APIRouter() 

@interfaceRoute.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("main_page.html", context={'request': request})

# ----------------------------------------------
# +++ ---------------- entity ------------------
@interfaceRoute.get("/entity/", response_class=HTMLResponse)
async def entity_list(request: Request, query_param: dict = Depends(qp_select_list)):
    return templates.TemplateResponse("entity/entity_list.html", context={'request': request, 'page': query_param['page']})

@interfaceRoute.get('/entity/{itemId}', response_class=HTMLResponse)
async def create_new_entity(request: Request, itemId: str):
    return templates.TemplateResponse("entity/entity_detail.html", context={'request': request, 'entity_iin': itemId})

# ----------------------------------------------
# employee
@interfaceRoute.get("/employee/", response_class=HTMLResponse)
async def employee_list(request: Request, query_param: dict = Depends(qp_select_list)):
    return templates.TemplateResponse("employee/employee_list.html", context={'request': request, 'page': query_param['page']})

@interfaceRoute.get('/employee/{itemId}', response_class=HTMLResponse)
async def create_new_employee(request: Request, itemId: str):
    return templates.TemplateResponse("employee/employee_detail.html", context={'request': request, 'employee_id': itemId})

# ----------------------------------------------
# counterparty
@interfaceRoute.get("/counterparty/", response_class=HTMLResponse)
async def counterparty_list(request: Request, query_param: dict = Depends(qp_select_list)):
    return templates.TemplateResponse("counterparty/counterparty_list.html", context={'request': request, 'page': query_param['page']})

@interfaceRoute.get("/counterparty/{itemId}", response_class=HTMLResponse)
async def counterparty_detail(request: Request, itemId: str):
    return templates.TemplateResponse("counterparty/counterparty_detail.html", context={'request': request, 'counterparty_iin': itemId})

# ----------------------------------------------
# approval_template
@interfaceRoute.get("/approval_template/", response_class=HTMLResponse)
async def approval_template_list(request: Request):
    listOfValue = await get_approval_template_list(nested = True, entity_iin = '') 
    return templates.TemplateResponse("approval_template/approval_template_list.html", context={'request': request, 'listOfValue': listOfValue})

@interfaceRoute.get("/approval_template/{itemId}", response_class=HTMLResponse)
async def approval_template_detail(request: Request, itemId: str):
    if(itemId=='new'):
        approval_template = ApprovalTemplate().asdict()
        return templates.TemplateResponse("approval_template/approval_template_detail.html", context={'request': request, 'approval_template': approval_template, 'itemId': itemId})    
    parametrs = {'nested': True}
    approval_template = await get_approval_template_by_id(int(itemId), **parametrs)
    return templates.TemplateResponse("approval_template/approval_template_detail.html", context={'request': request, 'approval_template': approval_template, 'itemId': int(itemId)})

# ----------------------------------------------
# purchase_requisition
@interfaceRoute.get("/purchase_requisition/", response_class=HTMLResponse)
async def purchase_requisition_list(request: Request):
    listOfValue = await get_purchase_requisition_list(nested = True, entity_iin = '') 
    return templates.TemplateResponse("purchase_requisition/purchase_requisition_list.html", context={'request': request, 'listOfValue': listOfValue})

@interfaceRoute.get("/purchase_requisition/{itemId}", response_class=HTMLResponse)
async def purchase_requisition_detail(request: Request, itemId: str):
    if(itemId=='new'):
        purchase_requisition = ApprovalTemplate().asdict()
        return templates.TemplateResponse("purchase_requisition/purchase_requisition_detail.html", context={'request': request, 'purchase_requisition': purchase_requisition, 'itemId': itemId})    
    parametrs = {'nested': True}
    purchase_requisition = await get_purchase_requisition_by_id(int(itemId), **parametrs)
    return templates.TemplateResponse("purchase_requisition/purchase_requisition_detail.html", context={'request': request, 'purchase_requisition': purchase_requisition, 'itemId': int(itemId)})

# ----------------------------------------------
# approval_process
@interfaceRoute.get("/approval_process/", response_class=HTMLResponse)
async def approval_process_list(request: Request):
    return templates.TemplateResponse("approval_process_rout/approval_process_rout_list.html", context={'request': request})

@interfaceRoute.get("/approval_process/{itemId}", response_class=HTMLResponse)
async def approval_process_detail(request: Request, itemId: str):
    return templates.TemplateResponse("approval_process_rout/approval_process_rout_detail.html", context={'request': request, 'itemId': int(itemId)})