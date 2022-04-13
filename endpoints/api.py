import email
from typing import List, Optional
from fastapi import APIRouter, Depends

from references.employee.urls import employeeRouter
from references.entity.urls import entityRouter
from references.business_type.urls import business_typeRouter
from references.notes.urls import notesRouter
from references.user.urls import userRouter
from references.counterparty.urls import counterpartyRouter

apiRouter = APIRouter()

apiRouter.include_router(prefix='/employee', router=employeeRouter)
apiRouter.include_router(prefix='/entity', router=entityRouter)
apiRouter.include_router(prefix='/business_type', router=business_typeRouter)
apiRouter.include_router(prefix='/notes', router=notesRouter)
apiRouter.include_router(prefix='/user', router=userRouter)
apiRouter.include_router(prefix='/counterparty', router=counterpartyRouter)


