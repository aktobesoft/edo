import random
from sqlalchemy import bindparam, column, desc, false, func, select, insert, text as sqlalchemy_text, tuple_, update, delete, String, desc
from core.db import database, SessionLocal
from common_module.urls_module import correct_datetime, correct_datetime
from documents.purchase_requisition_items.models import PurchaseRequisitionItems
from json import dumps, encoder
import hashlib
import binascii
  
async def get_pr_items_list_by_purchase_requisition_id(purchase_requisition_id: int):
    query_CTPurchaseRequisition = select(PurchaseRequisitionItems.id,
                                    func.row_number().over(
                                        partition_by=PurchaseRequisitionItems.purchase_requisition_id,
                                        order_by=PurchaseRequisitionItems.id).label('line_number'),
                                    PurchaseRequisitionItems.service,
                                    PurchaseRequisitionItems.description,
                                    PurchaseRequisitionItems.description_code,
                                    PurchaseRequisitionItems.quantity,
                                    PurchaseRequisitionItems.sum).\
                                        where(PurchaseRequisitionItems.purchase_requisition_id == purchase_requisition_id).\
                                        order_by(PurchaseRequisitionItems.id)
    records = await database.fetch_all(query_CTPurchaseRequisition) 
    listValue = []
    if records == None:
        listValue
    for rec in records:
        listValue.append(dict(rec))
    return listValue

async def update_pr_items_by_purchase_requisition(pr_items : list, purchase_requisition_id: int):
    
    listID = []
    listHashID = []
        
    for item in pr_items:
        dict_item = dict(item)
        listID.append(dict_item['id'])
        if dict_item['hash'] != '':
            listHashID.append(tuple_(dict_item['id'], dict_item['hash']))

    select1 = select(PurchaseRequisitionItems.id, PurchaseRequisitionItems.hash, func.lower("delete", type_=String).label('operation')).where(
                (PurchaseRequisitionItems.purchase_requisition_id == purchase_requisition_id) & (PurchaseRequisitionItems.id.not_in(listID)))
    
    select2 = select(PurchaseRequisitionItems.id, PurchaseRequisitionItems.hash, func.lower("no_update", type_=String)).where(
                (PurchaseRequisitionItems.purchase_requisition_id == purchase_requisition_id) & 
                (tuple_(PurchaseRequisitionItems.id, PurchaseRequisitionItems.hash).in_(listHashID)))
    
    query = select1.union_all(select2).alias('pr_list')
    result = await database.fetch_all(query)
    idListNoUpdate = []
    idListDelete = []

    listUpdate = []
    listInsert = []
    for item in result:
        if item['operation'] == 'delete':
            idListDelete.append(item['id'])    
        elif item['operation'] == 'no_update':
            idListNoUpdate.append(item['id'])

    rrIndex = random.randint(0, len(idListNoUpdate))
    index = 0
    
    for _pr_item in pr_items:
        pr_item = dict(_pr_item)
        if (pr_item['id'] in idListNoUpdate):
            if (index == rrIndex):
                # ?????????????????? ???????????????? ?????? ????????????
                # ???????????? ???????? ?????? ???? ???????????????? ???????????????????? ???????????????? ?????????? ?????????????? ?? ???????????????????????? ??????????????
                # ?????????? ?????????????????? ????????????
                # ???????? ?????????????????? ?????? ???????????? ?? ?????????? ????????????????
                copyRecord = dict(_pr_item)
                copyRecord.pop('hash')
                text = dumps(copyRecord, ensure_ascii=False, separators=(',', ':'))
                resultHash = binascii.crc32(text.encode('utf8'))
                if str(resultHash) != str(pr_item['hash']):
                    print('???????????????? ???????? ???? ?????????? {0} ?? {1}'.format(str(pr_item['hash']), resultHash))
            index = index + 1
            # continue
        elif (pr_item['id'] == 0):
            # ?? ???????????? ???????????? ???????????? ?????? ?????????? ???????????? ???????????? ?????? id ????????????
            # ???? ???????????? ???????????? ?????? ?????? ?????????? ????????????????????
            pr_item.pop('id')
            pr_item['purchase_requisition_id'] = purchase_requisition_id
            listInsert.append(pr_item)
        elif (pr_item['id'] not in idListDelete and pr_item['id'] not in idListNoUpdate):
            listUpdate.append(pr_item)

    if(len(listUpdate)>0):
        update_query = update(PurchaseRequisitionItems).\
        values(service=bindparam('service'), description=bindparam('description'), 
                description_code=bindparam('description_code'),
                quantity=bindparam('quantity'), sum=bindparam('sum'),
                hash = bindparam('hash')).\
        where((PurchaseRequisitionItems.id == bindparam('id')))
        result = await database.execute_many(str(update_query), listUpdate)
    
    if(len(listInsert)>0):
        result = await post_pr_items_by_purchase_requisition(listInsert, purchase_requisition_id)

    if(len(idListDelete)>0):
        result = await delete_pr_items_by_purchase_requisition(idListDelete, purchase_requisition_id)  

    return pr_items  


async def post_pr_items_by_purchase_requisition(pr_items : list, purchase_requisition_id: int):
    
    for pr_item in pr_items:
        pr_item['purchase_requisition_id'] = purchase_requisition_id

    query = insert(PurchaseRequisitionItems).\
            values(service = bindparam('service'), description = bindparam('description'), 
                    description_code = bindparam('description_code'),
                    quantity = bindparam('quantity'), sum = bindparam('sum'),
                    purchase_requisition_id = bindparam('purchase_requisition_id'),
                    hash = bindparam('hash'))
    result = await database.execute_many(str(query), pr_items) 

async def delete_pr_items_by_purchase_requisition(listID : list, purchase_requisition_id: int):

    # listID = [dict(item)['id'] for item in pr_items]
    query = delete(PurchaseRequisitionItems).\
            where((PurchaseRequisitionItems.purchase_requisition_id == purchase_requisition_id) & (PurchaseRequisitionItems.id.in_(listID)))
    result = await database.execute(query)

async def delete_all_pr_items_by_purchase_requisition(purchase_requisition_id: int):

    query = delete(PurchaseRequisitionItems).\
            where( PurchaseRequisitionItems.purchase_requisition_id == purchase_requisition_id)
    result = await database.execute(query)     

# insert(address_table).values(user_id=scalar_subq),
# ...         [
# ...             {"username": 'spongebob', "email_address": "spongebob@sqlalchemy.org"},
# ...             {"username": 'sandy', "email_address": "sandy@sqlalchemy.org"},
# ...             {"username": 'sandy', "email_address": "sandy@squirrelpower.org"},
# ...         ]

# >>> from sqlalchemy import bindparam
# >>> stmt = (
# ...   update(user_table).
# ...   where(user_table.c.name == bindparam('oldname')).
# ...   values(name=bindparam('newname'))
# ... )
# >>> with engine.begin() as conn:
# ...   conn.execute(
# ...       stmt,
# ...       [
# ...          {'oldname':'jack', 'newname':'ed'},
# ...          {'oldname':'wendy', 'newname':'mary'},
# ...          {'oldname':'jim', 'newname':'jake'},
# ...       ]
# ...   )
# BEGIN (