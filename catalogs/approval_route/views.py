from sqlalchemy import String, bindparam, func, select, insert, tuple_, update, delete
import asyncpg
from catalogs.approval_process.models import ApprovalProcess
from catalogs.approval_status.models import ApprovalStatus
from catalogs.document_type.views import get_document_type_id_by_metadata_name
from core.db import database
from common_module.urls_module import correct_datetime, is_need_filter

from catalogs.approval_route.models import ApprovalRoute, ApprovalRouteIn
from catalogs.user.models import User, User, user_fillDataFromDict

async def get_approval_route_by_id(approval_route_id: int):
    query = select(ApprovalRoute,
            ApprovalStatus.id.label('status_id'),
            ApprovalStatus.date.label('status_date'),
            ApprovalStatus.status.label('status'),
            ApprovalStatus.comment.label('status_comment')).\
            join(ApprovalStatus, ApprovalRoute.id == ApprovalStatus.id, isouter=True).\
                where(ApprovalRoute.id == approval_route_id)
    result = await database.fetch_one(query)
    return result

async def get_approval_route_by_aproval_process_id(aproval_process_id: int):
    query = select(ApprovalRoute,
            ApprovalStatus.id.label('status_id'),
            ApprovalStatus.date.label('status_date'),
            ApprovalStatus.status.label('status'),
            ApprovalStatus.comment.label('status_comment')).\
            join(ApprovalStatus, (ApprovalRoute.id == ApprovalStatus.id) & (ApprovalStatus.is_active), isouter=True).\
                where(ApprovalRoute.approval_process_id == aproval_process_id).order_by(ApprovalRoute.id)
    
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def get_approval_route_nested_by_aproval_process_id(aproval_process_id: int):
    query = select(ApprovalRoute,
            ApprovalStatus.id.label('status_id'),
            ApprovalStatus.date.label('status_date'),
            ApprovalStatus.status.label('status'),
            ApprovalStatus.comment.label('status_comment'),
            User.id.label('user_id'),
            User.email.label('user_email'),
            User.name.label('user_name')).\
            join(User, ApprovalRoute.user_id == User.id, isouter=True).\
            join(ApprovalStatus, (ApprovalRoute.id == ApprovalStatus.approval_route_id) & (ApprovalRoute.user_id == ApprovalStatus.user_id)\
                & (ApprovalStatus.is_active), isouter=True).\
                where(ApprovalRoute.approval_process_id == aproval_process_id).order_by(ApprovalRoute.id)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        recordDict['user'] = user_fillDataFromDict(recordDict)
        listValue.append(recordDict)
    return listValue

async def get_approval_route_nested_by_id(approval_route_id: int):
    query = select(ApprovalRoute).where(ApprovalRoute.id == approval_route_id)
    result = await database.fetch_one(query)
    return result

async def delete_approval_route_by_id(approval_route_list_id: list):
    query = delete(ApprovalRoute).where(ApprovalRoute.id.in_(approval_route_list_id))
    result = await database.execute(query)
    return result

async def delete_approval_routes_by_approval_process_id(approval_process_id: int):
    query = delete(ApprovalRoute).where(ApprovalRoute.approval_process_id == approval_process_id)
    result = await database.execute(query)
    return result

async def get_approval_route_list(limit: int = 100,skip: int = 0,**kwargs):

    query = select(ApprovalRoute).limit(limit).offset(skip)
    records = await database.fetch_all(query)
    listValue = []
    for rec in records:
        recordDict = dict(rec)
        listValue.append(recordDict)
    return listValue

async def get_approval_routes_by_metadata(metadata_name: str, **kwargs):
    metadata_name_document_type_id = await get_document_type_id_by_metadata_name(metadata_name)
    query_min = select(func.min(ApprovalRoute.level).label("min_level"),
                        ApprovalProcess.id.label("approval_process_id")).\
                    join(ApprovalRoute, (ApprovalProcess.id == ApprovalRoute.approval_process_id) & (ApprovalRoute.is_active), isouter=True).\
                    join(ApprovalStatus, (ApprovalRoute.id == ApprovalStatus.approval_route_id) & (ApprovalStatus.is_active), isouter=True).\
                    where((ApprovalProcess.is_active) & (ApprovalStatus.status == None) & (ApprovalProcess.document_type_id == metadata_name_document_type_id)).\
                    group_by(ApprovalProcess.id)
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query_min = query_min.where(ApprovalProcess.entity_iin.in_(kwargs['entity_iin_list']))

    query_current_approval_routes = select(
            func.lower("current_approval_routes", type_=String).label('list_type'), 
            ApprovalRoute.user_id,
            ApprovalRoute.level,
            ApprovalRoute.type,
            ApprovalProcess.id.label('approval_process_id'),
            ApprovalRoute.id.label('route_id'),
            ApprovalStatus.status.label('route_status'),
            ApprovalStatus.comment.label('route_comment'),
            ApprovalStatus.date.label('route_date')).\
            join(ApprovalRoute, (ApprovalProcess.id == ApprovalRoute.approval_process_id) & (ApprovalRoute.is_active), isouter=True).\
            join(ApprovalStatus, (ApprovalRoute.id == ApprovalStatus.approval_route_id) & (ApprovalStatus.is_active), isouter=True).\
            where((ApprovalProcess.is_active)  & (ApprovalProcess.document_type_id == metadata_name_document_type_id)).\
            where(tuple_(ApprovalRoute.level, ApprovalRoute.approval_process_id).in_(query_min))
    

    query_all_approval_routes = select(
            func.lower("all_approval_routes", type_=String).label('list_type'), 
            ApprovalRoute.user_id,
            ApprovalRoute.level,
            ApprovalRoute.type,
            ApprovalProcess.id.label('approval_process_id'),
            ApprovalRoute.id.label('route_id'),
            ApprovalStatus.status.label('route_status'),
            ApprovalStatus.comment.label('route_comment'),
            ApprovalStatus.date.label('route_date')).\
            join(ApprovalRoute, (ApprovalProcess.id == ApprovalRoute.approval_process_id) & (ApprovalRoute.is_active), isouter=True).\
            join(ApprovalStatus, (ApprovalRoute.id == ApprovalStatus.approval_route_id) & (ApprovalStatus.is_active), isouter=True).\
            where((ApprovalProcess.is_active) & (ApprovalProcess.document_type_id == metadata_name_document_type_id))
            
            # where(ApprovalRoute.approval_process_id).in_(kwargs['approval_process_id_list'])
    # RLS
    if(is_need_filter('entity_iin_list', kwargs)):
        query_all_approval_routes = query_all_approval_routes.where(ApprovalProcess.entity_iin.in_(kwargs['entity_iin_list']))
    
    query = query_current_approval_routes.union_all(query_all_approval_routes).alias('approval_route_list')           
    # print(query)
    records = await database.fetch_all(query)
    dictValue = {}
    
    for rec in records:
        recordDict = dict(rec)
        if(recordDict['approval_process_id'] not in dictValue):
            dictValue[recordDict['approval_process_id']] = {'current_approval_routes': [], 'all_approval_routes': []}
        
        if(recordDict['list_type']=='current_approval_routes'):
            dictValue[recordDict['approval_process_id']]['current_approval_routes'].append(recordDict)
        elif(recordDict['list_type']=='all_approval_routes'):
            dictValue[recordDict['approval_process_id']]['all_approval_routes'].append(recordDict)
        
    return dictValue

async def post_approval_route(arInstance : dict):
    
    query = insert(ApprovalRoute).values(
                is_active = arInstance["is_active"], 
                level = int(arInstance["level"]),
                type = arInstance["type"],
                document_id = int(arInstance["document_id"]),
                entity_iin = arInstance["entity_iin"],
                user_id = int(arInstance["user_id"]),
                approval_template_id = int(arInstance["approval_template_id"]),
                hash = arInstance["hash"],
                approval_process_id = int(arInstance["approval_process_id"]))
    result = await database.execute(query)
    return {**arInstance, 'id': result}

async def post_approval_routes_by_approval_process_id(arList : list):
    
    query = insert(ApprovalRoute).values(
                is_active = bindparam("is_active"), 
                level = bindparam("level"),
                type = bindparam("type"),
                document_id = bindparam("document_id"),
                entity_iin = bindparam("entity_iin"),
                user_id = bindparam("user_id"),
                approval_template_id = bindparam("approval_template_id"),
                hash = bindparam("hash"),
                approval_process_id = bindparam("approval_process_id"))
    result = await database.execute_many(query, arList)
    return {result}

async def update_approval_route(arInstance: dict, approval_route_id: int):

    query = update(ApprovalRoute).values(
                is_active = arInstance["is_active"], 
                level = int(arInstance["level"]),
                type = arInstance["type"],
                document_id = int(arInstance["document_id"]),
                entity_iin = arInstance["entity_iin"],
                user_id = int(arInstance["user_id"]),
                approval_template_id = int(arInstance["approval_template_id"]),
                hash = bindparam("hash"),
                approval_process_id = int(arInstance["approval_process_id"])).\
                    where(ApprovalRoute.id == approval_route_id)

    result = await database.execute(query)
    return arInstance

async def update_approval_routes_by_approval_process_id(ap_routes : list, approval_process_id: int):

    listID = []
    listHashID = []
    newList = []

    # Надо подумать нужна ли хэш функция
    # чтобы избежать обновления всех данных
    # посути данных должно быть не так много
    # но все же
    
    for ap_route in ap_routes:
        ap_route_dict = dict(ap_route)
        listID.append(ap_route_dict['id'])
        ap_route_dict['approval_process_id'] = approval_process_id
        newList.append(ap_route_dict)
        # listHashID.append(tuple_(dict_item['id'], dict_item['hash']))

        
    select1 = select(ApprovalRoute.id, ApprovalRoute.hash, func.lower("delete", type_= String).label('operation')).where(
                (ApprovalRoute.approval_process_id == approval_process_id) & (ApprovalRoute.id.not_in(listID)))
    
    # select2 = select(ApprovalRoute.id, ApprovalRoute.hash, func.lower("no_update", type_=String)).where(
    #             (ApprovalRoute.approval_process_id == approval_process_id) & 
    #             (tuple_(ApprovalRoute.id, ApprovalRoute.hash).in_(listHashID)))
    
    # query = select1.union_all(select2).alias('pr_list')
    result = await database.fetch_all(select1)
    idListNoUpdate = []
    idListDelete = []

    listUpdate = []
    listInsert = []
    for item in result:
        if item['operation'] == 'delete':
            idListDelete.append(item['id'])    
        elif item['operation'] == 'no_update':
            idListNoUpdate.append(item['id'])

    # rrIndex = random.randint(0, len(idListNoUpdate))
    # index = 0
    
    for _at_step in ap_routes:
        at_step = dict(_at_step)
        if (at_step['id'] in idListNoUpdate):
            # if (index == rrIndex):
            #     # рандомная проверка хэш записи
            #     # защита если кто то пытается специально посылать много записей с неправильной функции
            #     # чтобы загрузить сервис
            #     # надо придумать что делать в такой ситуации
            #     copyRecord = dict(_at_step)
            #     copyRecord.pop('hash')
            #     text = dumps(copyRecord, ensure_ascii=False, separators=(',', ':'))
            #     resultHash = binascii.crc32(text.encode('utf8'))
            #     if str(resultHash) != str(at_step['hash']):
            #         print('Внимание хэши не равны {0} и {1}'.format(str(at_step['hash']), resultHash))
            # index = index + 1
            continue
        elif (at_step['id'] == 0):
            # в первую запись всегда хэш будет другой потому как id пустой
            # во второй проход хэш уже будет правильный
            at_step.pop('id')
            at_step['approval_process_id'] = approval_process_id
            listInsert.append(at_step)
        elif (at_step['id'] not in idListDelete and at_step['id'] not in idListNoUpdate):
            at_step['approval_process_id'] = approval_process_id
            listUpdate.append(at_step)

    if(len(listUpdate)>0):
        update_query = update(ApprovalRoute).values(
                is_active = bindparam("is_active"), 
                level = bindparam("level"),
                type = bindparam("type"),
                document_id = bindparam("document_id"),
                document_type_id = (bindparam("document_type_id")),
                entity_iin = bindparam("entity_iin"),
                hash = bindparam("hash"), 
                user_id = bindparam("user_id"),
                approval_template_id = bindparam("approval_template_id")).\
                     where((ApprovalRoute.approval_process_id == bindparam("approval_process_id")) & (ApprovalRoute.id == bindparam("id")))
        result = await database.execute_many(str(update_query), newList)
    
    if(len(listInsert)>0):
        result = await post_approval_routes_by_approval_process_id(listInsert)

    if(len(idListDelete)>0):
        result = await delete_approval_route_by_id(idListDelete)  

    return ap_routes 