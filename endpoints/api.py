import email
from typing import List, Optional
from fastapi import APIRouter, Depends

from catalogs.employee.urls import employeeRouter
from catalogs.entity.urls import entityRouter
from catalogs.notes.urls import notesRouter
from catalogs.user.urls import userRouter
from catalogs.counterparty.urls import counterpartyRouter
from catalogs.approval_template.urls import approval_templateRouter
from catalogs.approval_template_step.urls import approval_template_stepRouter
from catalogs.approval_process.urls import approval_processRouter
from catalogs.approval_status.urls import approval_statusRouter
from catalogs.enum_types.urls import enum_typeRouter
from catalogs.task_status.urls import task_statusRouter

from documents.purchase_requisition.urls import purchase_requisitionRouter
from documents.employee_task.urls import employee_taskRouter

apiRouter = APIRouter()

apiRouter.include_router(prefix='/employee', router = employeeRouter,  tags = ["employee"])
apiRouter.include_router(prefix='/entity', router = entityRouter,  tags = ["entity"])
apiRouter.include_router(prefix='/notes', router = notesRouter,  tags = ["notes"])
apiRouter.include_router(prefix='/user', router = userRouter,  tags = ["user"])
apiRouter.include_router(prefix='/counterparty', router = counterpartyRouter,  tags = ["counterparty"])
apiRouter.include_router(prefix='/purchase_requisition', router = purchase_requisitionRouter,  tags = ["purchase_requisition"])
apiRouter.include_router(prefix='/employee_task', router = employee_taskRouter,  tags = ["employee_task"])
apiRouter.include_router(prefix='/approval_template', router = approval_templateRouter,  tags = ["approval_template"])
apiRouter.include_router(prefix='/approval_template_step', router = approval_template_stepRouter,  tags = ["approval_template_step"])
apiRouter.include_router(prefix='/approval_process', router = approval_processRouter,  tags = ["approval_process"])
apiRouter.include_router(prefix='/approval_status', router = approval_statusRouter,  tags = ["approval_status"])
apiRouter.include_router(prefix='/task_status', router = task_statusRouter,  tags = ["task_status"])
apiRouter.include_router(prefix='/enum_types', router = enum_typeRouter,  tags = ["enum_types"])



