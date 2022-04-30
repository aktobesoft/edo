from sqlalchemy import bindparam, desc, func, select, insert, update, delete
from core.db import database
from common_module.urls_module import correct_datetime, correct_datetime
from documents.purchase_requisition_items.models import PurchaseRequisitionItems
from json import dumps


async def get_pr_items_list_by_purchase_requisition_id(purchase_requisition_id: int, **kwargs):
    query_CTPurchaseRequisition = select(PurchaseRequisitionItems.id,
                                    func.row_number().over(
                                        partition_by=PurchaseRequisitionItems.purchase_requisition_id,
                                        order_by=desc(PurchaseRequisitionItems.purchase_requisition_id)).label('line_number'),
                                    PurchaseRequisitionItems.service,
                                    PurchaseRequisitionItems.description,
                                    PurchaseRequisitionItems.description_code,
                                    PurchaseRequisitionItems.quantity,
                                    PurchaseRequisitionItems.sum).\
                                        where(PurchaseRequisitionItems.purchase_requisition_id == purchase_requisition_id)
    records = await database.fetch_all(query_CTPurchaseRequisition) 
    listValue = []
    if records == None:
        listValue
    for rec in records:
        listValue.append(dict(rec))
    return listValue

async def post_pr_items_by_purchase_requisition(pr_items : list):
    
    listID = [dict(item)['id'] for item in pr_items]
    query = select(PurchaseRequisitionItems).where(PurchaseRequisitionItems.id.in_(listID))
    result = await database.fetch_all(query)
    update_query = update(PurchaseRequisitionItems).\
        values(service=bindparam('service'), description=bindparam('description'), 
                description_code=bindparam('description_code'),
                quantity=bindparam('quantity'), sum=bindparam('sum')).\
        where(PurchaseRequisitionItems.id == bindparam('id'))
    valueList = []
    for pr_item in pr_items:
        #for exist_item in result:
        valueList.append(dict(pr_item))
    # newVal = dict(pr_items[0])
    # dictVal = [{
    #     "id": newVal['id'],
    #     'service': newVal['service'],
    #     'description': newVal['description'],
    #     'description_code': newVal['description_code'],
    #     'quantity': newVal['quantity'],
    #     'sum': newVal['sum']
    # }]
    # print(dictVal)
    print(update_query)
    newPurchaseRequisitionId = await database.execute_many(str(update_query), valueList)

    return pr_items


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