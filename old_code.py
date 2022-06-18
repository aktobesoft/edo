# async def get_purchase_requisition_nested_list_with_routs(**kwargs):
#     purchase_requisition_document_type_id = await get_document_type_id_by_metadata_name("purchase_requisition")
#     query = select( 
#             ApprovalRoute.employee_id,
#             ApprovalRoute.level,
#             ApprovalRoute.type,
#             ApprovalRoute.approval_process_id,
#             ApprovalRoute.id.label('route_id'),
#             ApprovalStatus.status.label('route_status'),
#             ApprovalStatus.comment.label('route_comment'),
#             ApprovalStatus.date.label('route_date'),
#             PurchaseRequisition.id, 
#             PurchaseRequisition.document_type_id, 
#             PurchaseRequisition.guid, 
#             PurchaseRequisition.number, 
#             PurchaseRequisition.date, 
#             PurchaseRequisition.comment, 
#             PurchaseRequisition.sum, 
#             PurchaseRequisition.counterparty_iin.label('counterparty_iin'), 
#             PurchaseRequisition.document_type_id.label('document_type_id'), 
#             PurchaseRequisition.entity_iin.label('entity_iin'),
#             Entity.name.label("entity_name"),
#             Entity.id.label("entity_id"),
#             Counterparty.id.label("counterparty_id"), 
#             Counterparty.name.label("counterparty_name"),
#             DocumentType.name.label("document_type_name"),
#             DocumentType.description.label("document_type_description"),
#             ApprovalProcess.status.label('process_status'),
#             ApprovalProcess.id.label("process_id")).\
#                 join(ApprovalStatus, (ApprovalRoute.id == ApprovalStatus.approval_route_id) & (ApprovalRoute.is_active), isouter=True).\
#                 join(PurchaseRequisition, (ApprovalRoute.document_id == PurchaseRequisition.id) & 
#                     (ApprovalRoute.document_type_id == PurchaseRequisition.document_type_id) & (ApprovalRoute.is_active), isouter=True).\
#                 join(Entity, PurchaseRequisition.entity_iin == Entity.iin, isouter=True).\
#                 join(Counterparty, PurchaseRequisition.counterparty_iin == Counterparty.iin, isouter=True).\
#                 join(DocumentType, PurchaseRequisition.document_type_id == DocumentType.id, isouter=True).\
#                 join(ApprovalProcess, (PurchaseRequisition.id == ApprovalProcess.document_id) & 
#                     (PurchaseRequisition.document_type_id == ApprovalProcess.document_type_id) & (ApprovalProcess.is_active), isouter=True).\
#                 order_by(ApprovalRoute.document_id, ApprovalRoute.level, ApprovalRoute.type)
#     # RLS
#     if(is_need_filter('entity_iin_list', kwargs)):
#         query = query.where(ApprovalRoute.entity_iin.in_(kwargs['entity_iin_list']))
    
#     if('employee_id' in kwargs):
#         query = query.where(ApprovalRoute.employee_id == kwargs['employee_id'])
#     print(query)
#     records = await database.fetch_all(query)
#     listValue = []
#     for rec in records:
#         recordDict = dict(rec)
#         recordDict['entity'] = entity_fillDataFromDict(rec)
#         recordDict['document_type'] = document_type_fillDataFromDict(rec)
#         recordDict['counterparty'] = counterparty_fillDataFromDict(rec)
#         listValue.append(recordDict)
#     return listValue

#     async def get_purchase_requisition_nested_list_with_routes(**kwargs):
#     purchase_requisition_document_type_id = await get_document_type_id_by_metadata_name("purchase_requisition")
#     query_min = select(func.min(ApprovalRoute.level).label("min_level"),
#                         ApprovalProcess.id.label("approval_process_id")).\
#                     join(ApprovalRoute, (ApprovalProcess.id == ApprovalRoute.approval_process_id) & (ApprovalRoute.is_active), isouter=True).\
#                     join(ApprovalStatus, (ApprovalRoute.id == ApprovalStatus.approval_route_id) & (ApprovalStatus.is_active), isouter=True).\
#                     where((ApprovalProcess.is_active) & (ApprovalStatus.status == None)).\
#                     group_by(ApprovalProcess.id)
#     # RLS
#     if(is_need_filter('entity_iin_list', kwargs)):
#         query_min = query_min.where(ApprovalProcess.entity_iin.in_(kwargs['entity_iin_list']))

#     query_current_approval_routes = select(
#             func.lower("current_approval_routes", type_=String).label('list_type'), 
#             ApprovalRoute.employee_id,
#             ApprovalRoute.level,
#             ApprovalRoute.type,
#             ApprovalProcess.id.label('approval_process_id'),
#             ApprovalRoute.id.label('route_id'),
#             ApprovalStatus.status.label('route_status'),
#             ApprovalStatus.comment.label('route_comment'),
#             ApprovalStatus.date.label('route_date')).\
#             join(ApprovalRoute, (ApprovalProcess.id == ApprovalRoute.approval_process_id) & (ApprovalRoute.is_active), isouter=True).\
#             join(ApprovalStatus, (ApprovalRoute.id == ApprovalStatus.approval_route_id) & (ApprovalStatus.is_active), isouter=True).\
#             where(ApprovalProcess.is_active).\
#             where(tuple_(ApprovalRoute.level, ApprovalRoute.approval_process_id).in_(query_min))
    

#     query_all_approval_routes = select(
#             func.lower("all_approval_routes", type_=String).label('list_type'), 
#             ApprovalRoute.employee_id,
#             ApprovalRoute.level,
#             ApprovalRoute.type,
#             ApprovalProcess.id.label('approval_process_id'),
#             ApprovalRoute.id.label('route_id'),
#             ApprovalStatus.status.label('route_status'),
#             ApprovalStatus.comment.label('route_comment'),
#             ApprovalStatus.date.label('route_date')).\
#             join(ApprovalRoute, (ApprovalProcess.id == ApprovalRoute.approval_process_id) & (ApprovalRoute.is_active), isouter=True).\
#             join(ApprovalStatus, (ApprovalRoute.id == ApprovalStatus.approval_route_id) & (ApprovalStatus.is_active), isouter=True).\
#             where(ApprovalProcess.is_active)
            
#             # where(ApprovalRoute.approval_process_id).in_(kwargs['approval_process_id_list'])
#     # RLS
#     if(is_need_filter('entity_iin_list', kwargs)):
#         query_all_approval_routes = query_all_approval_routes.where(ApprovalProcess.entity_iin.in_(kwargs['entity_iin_list']))

#     query = query_current_approval_routes.union_all(query_all_approval_routes).alias('approval_route_list')           
    
#     print(query)
#     records = await database.fetch_all(query)
#     dictValue = {}
    
#     for rec in records:
#         recordDict = dict(rec)
#         if(recordDict['approval_process_id'] not in dictValue):
#             dictValue[recordDict['approval_process_id']] = {'current_approval_routes': [], 'all_approval_routes': []}
        
#         if(recordDict['list_type']=='current_approval_routes'):
#             dictValue[recordDict['approval_process_id']]['current_approval_routes'].append(recordDict)
#         elif(recordDict['list_type']=='all_approval_routes'):
#             dictValue[recordDict['approval_process_id']]['all_approval_routes'].append(recordDict)
        
#     return dictValue



#     # -------------------------------------------------------------------

#         query_current_approval_routes = select(
#             func.lower("current_approval_routes", type_=String).label('list_type'), 
#             ApprovalProcess.id.label('approval_process_id'),
#             ApprovalProcess.status.label('process_status'),
#             ApprovalRoute.employee_id,
#             ApprovalRoute.level,
#             ApprovalRoute.type,
#             ApprovalRoute.id.label('route_id'),
#             ApprovalStatus.status.label('route_status'),
#             ApprovalStatus.comment.label('route_comment'),
#             ApprovalStatus.date.label('route_date'),
#             PurchaseRequisition.id, 
#             PurchaseRequisition.document_type_id, 
#             PurchaseRequisition.guid, 
#             PurchaseRequisition.number, 
#             PurchaseRequisition.date, 
#             PurchaseRequisition.comment, 
#             PurchaseRequisition.sum, 
#             PurchaseRequisition.counterparty_iin.label('counterparty_iin'), 
#             PurchaseRequisition.document_type_id.label('document_type_id'), 
#             PurchaseRequisition.entity_iin.label('entity_iin'),
#             Entity.name.label("entity_name"),
#             Entity.id.label("entity_id"),
#             Counterparty.id.label("counterparty_id"), 
#             Counterparty.name.label("counterparty_name"),
#             DocumentType.name.label("document_type_name"),
#             DocumentType.description.label("document_type_description")).\
#             join(ApprovalRoute, (ApprovalProcess.id == ApprovalRoute.approval_process_id) & (ApprovalRoute.is_active), isouter=True).\
#             join(PurchaseRequisition, (ApprovalProcess.document_id == PurchaseRequisition.id) & 
#                     (ApprovalProcess.document_type_id == PurchaseRequisition.document_type_id) & (ApprovalProcess.is_active), isouter=True).\
#             join(ApprovalStatus, (ApprovalRoute.id == ApprovalStatus.approval_route_id) & (ApprovalStatus.is_active), isouter=True).\
#             join(Entity, PurchaseRequisition.entity_iin == Entity.iin, isouter=True).\
#             join(Counterparty, PurchaseRequisition.counterparty_iin == Counterparty.iin, isouter=True).\
#             join(DocumentType, PurchaseRequisition.document_type_id == DocumentType.id, isouter=True).\
#             where(ApprovalProcess.is_active).\
#             where(tuple_(ApprovalRoute.level, ApprovalRoute.approval_process_id).in_(query_min))
    

#     query_all_approval_routes = select(
#             func.lower("all_approval_routes", type_=String).label('list_type'), 
#             ApprovalProcess.id.label('approval_process_id'),
#             ApprovalProcess.status.label('process_status'),
#             ApprovalRoute.employee_id,
#             ApprovalRoute.level,
#             ApprovalRoute.type,
#             ApprovalRoute.id.label('route_id'),
#             ApprovalStatus.status.label('route_status'),
#             ApprovalStatus.comment.label('route_comment'),
#             ApprovalStatus.date.label('route_date'),
#             PurchaseRequisition.id, 
#             PurchaseRequisition.document_type_id, 
#             PurchaseRequisition.guid, 
#             PurchaseRequisition.number, 
#             PurchaseRequisition.date, 
#             PurchaseRequisition.comment, 
#             PurchaseRequisition.sum, 
#             PurchaseRequisition.counterparty_iin.label('counterparty_iin'), 
#             PurchaseRequisition.document_type_id.label('document_type_id'), 
#             PurchaseRequisition.entity_iin.label('entity_iin'),
#             Entity.name.label("entity_name"),
#             Entity.id.label("entity_id"),
#             Counterparty.id.label("counterparty_id"), 
#             Counterparty.name.label("counterparty_name"),
#             DocumentType.name.label("document_type_name"),
#             DocumentType.description.label("document_type_description")).\
#             join(ApprovalRoute, (ApprovalProcess.id == ApprovalRoute.approval_process_id) & (ApprovalRoute.is_active), isouter=True).\
#             join(PurchaseRequisition, (ApprovalProcess.document_id == PurchaseRequisition.id) & 
#                     (ApprovalProcess.document_type_id == PurchaseRequisition.document_type_id) & (ApprovalProcess.is_active), isouter=True).\
#             join(ApprovalStatus, (ApprovalRoute.id == ApprovalStatus.approval_route_id) & (ApprovalStatus.is_active), isouter=True).\
#             join(Entity, PurchaseRequisition.entity_iin == Entity.iin, isouter=True).\
#             join(Counterparty, PurchaseRequisition.counterparty_iin == Counterparty.iin, isouter=True).\
#             join(DocumentType, PurchaseRequisition.document_type_id == DocumentType.id, isouter=True).\
#             where(ApprovalProcess.is_active)