from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, Request
from common_module.urls_module import qp_select_list
from fastapi.templating import Jinja2Templates
from documents.purchase_requisition.views import get_purchase_requisition_list
from catalogs.approval_template.views import get_approval_template_list

from catalogs.enum_types.models import StepType

templates = Jinja2Templates(directory="templates")
interfaceRoute = APIRouter() 

@interfaceRoute.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("main_page.html", context={'request': request})

@interfaceRoute.get("/auth", response_class=HTMLResponse)
async def auth_page(request: Request):
    return templates.TemplateResponse("auth_page.html", context={'request': request})

# ----------------------------------------------
# entity
@interfaceRoute.get("/entity/", response_class=HTMLResponse)
async def entity_list(request: Request, parameters: dict = Depends(qp_select_list)):
    return templates.TemplateResponse("entity/entity_list.html", context={'request': request, 'page': parameters['page']})

@interfaceRoute.get('/entity/{itemId}', response_class=HTMLResponse)
async def create_new_entity(request: Request, itemId: str):
    return templates.TemplateResponse("entity/entity_detail.html", context={'request': request, 'entity_iin': itemId})

# ----------------------------------------------
# employee
@interfaceRoute.get("/employee/", response_class=HTMLResponse)
async def employee_list(request: Request, parameters: dict = Depends(qp_select_list)):
    return templates.TemplateResponse("employee/employee_list.html", context={'request': request, 'page': parameters['page']})

@interfaceRoute.get('/employee/{itemId}', response_class=HTMLResponse)
async def create_new_employee(request: Request, itemId: str):
    return templates.TemplateResponse("employee/employee_detail.html", context={'request': request, 'employee_id': itemId})

# ----------------------------------------------
# user
@interfaceRoute.get("/user/", response_class=HTMLResponse)
async def user_list(request: Request, parameters: dict = Depends(qp_select_list)):
    return templates.TemplateResponse("user/user_list.html", context={'request': request, 'page': parameters['page']})

@interfaceRoute.get('/user/{itemId}', response_class=HTMLResponse)
async def create_new_user(request: Request, itemId: str):
    return templates.TemplateResponse("user/user_detail.html", context={'request': request, 'user_id': itemId})

# ----------------------------------------------
# counterparty
@interfaceRoute.get("/counterparty/", response_class=HTMLResponse)
async def counterparty_list(request: Request, parameters: dict = Depends(qp_select_list)):
    return templates.TemplateResponse("counterparty/counterparty_list.html", context={'request': request, 'page': parameters['page']})

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
    return templates.TemplateResponse("approval_template/approval_template_detail.html", context={'request': request, 'itemId': itemId})

# ----------------------------------------------
# purchase_requisition
@interfaceRoute.get("/purchase_requisition/", response_class=HTMLResponse)
async def purchase_requisition_list(request: Request):
    listOfValue = await get_purchase_requisition_list(nested = True, entity_iin = '') 
    return templates.TemplateResponse("purchase_requisition/purchase_requisition_list.html", context={'request': request, 'listOfValue': listOfValue})

@interfaceRoute.get("/purchase_requisition/{itemId}", response_class=HTMLResponse)
async def purchase_requisition_detail(request: Request, itemId: str):
    return templates.TemplateResponse("purchase_requisition/purchase_requisition_detail.html", context={'request': request, 'itemId': itemId})

# ----------------------------------------------
# approval_process
@interfaceRoute.get("/approval_process/", response_class=HTMLResponse)
async def approval_process_list(request: Request):
    return templates.TemplateResponse("approval_process_rout/approval_process_rout_list.html", context={'request': request})

@interfaceRoute.get("/approval_process/{itemId}", response_class=HTMLResponse)
async def approval_process_detail(request: Request, itemId: str):
    return templates.TemplateResponse("approval_process_rout/approval_process_rout_detail.html", context={'request': request, 'itemId': int(itemId)})