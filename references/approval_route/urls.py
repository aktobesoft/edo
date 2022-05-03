from fastapi import APIRouter, Depends
from common_module.urls_module import qp_select_list
from typing import List, Union

from references.approval_route.models import ApprovalRoute, ApprovalRouteIn, ApprovalRouteOut
from references.approval_route import views


approval_routeRouter = APIRouter()

@approval_routeRouter.get('/', response_model = list[ApprovalRouteOut])
async def get_approval_route_list(commons: dict = Depends(qp_select_list)):
    records = await views.get_approval_route_list(**commons)
    return records

@approval_routeRouter.get('/{approval_route_id}')
async def get_approval_route_by_id(approval_route_id : int):
    result = await views.get_approval_route_by_id(approval_route_id)
    return result

@approval_routeRouter.post('/', response_model = ApprovalRouteOut)
async def post_approval_route(approval_routeInstance : ApprovalRouteIn):
    businessTypeDict = approval_routeInstance.dict()
    result = await views.post_approval_route(businessTypeDict)
    return result

@approval_routeRouter.put('/', response_model = ApprovalRouteOut)
async def update_approval_route(newApprovalRouteIn : ApprovalRouteOut):
    newApprovalRouteIn = dict(newApprovalRouteIn)
    result = await views.update_approval_route(newApprovalRouteIn)
    return newApprovalRouteIn

@approval_routeRouter.delete('/{approval_route_id}')
async def delete_approval_route_by_id(approval_route_id : int):
    result = await views.delete_approval_route_by_id(approval_route_id)
    return result