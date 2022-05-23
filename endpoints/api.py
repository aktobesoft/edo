import email
from typing import List, Optional
from fastapi import APIRouter, Depends

from catalogs.employee.urls import employeeRouter
from catalogs.entity.urls import entityRouter
from catalogs.business_type.urls import business_typeRouter
from catalogs.notes.urls import notesRouter
from catalogs.user.urls import userRouter
from catalogs.counterparty.urls import counterpartyRouter
from documents.purchase_requisition.urls import purchase_requisitionRouter
from catalogs.approval_template.urls import approval_templateRouter
from catalogs.approval_template_step.urls import approval_template_stepRouter
from catalogs.approval_process.urls import approval_processRouter
from catalogs.document_type.urls import document_typeRouter
from catalogs.approval_status.urls import approval_statusRouter


apiRouter = APIRouter()

apiRouter.include_router(prefix='/employee', router = employeeRouter,  tags = ["employee"])
apiRouter.include_router(prefix='/entity', router = entityRouter,  tags = ["entity"])
apiRouter.include_router(prefix='/business_type', router = business_typeRouter,  tags = ["business_type"])
apiRouter.include_router(prefix='/notes', router = notesRouter,  tags = ["notes"])
apiRouter.include_router(prefix='/user', router = userRouter,  tags = ["user"])
apiRouter.include_router(prefix='/counterparty', router = counterpartyRouter,  tags = ["counterparty"])
apiRouter.include_router(prefix='/purchase_requisition', router = purchase_requisitionRouter,  tags = ["purchase_requisition"])
apiRouter.include_router(prefix='/document_type', router = document_typeRouter,  tags = ["document_type"])
apiRouter.include_router(prefix='/approval_template', router = approval_templateRouter,  tags = ["approval_template"])
apiRouter.include_router(prefix='/approval_template_step', router = approval_template_stepRouter,  tags = ["approval_template_step"])
apiRouter.include_router(prefix='/approval_process', router = approval_processRouter,  tags = ["approval_process"])
apiRouter.include_router(prefix='/approval_status', router = approval_statusRouter,  tags = ["approval_status"])



