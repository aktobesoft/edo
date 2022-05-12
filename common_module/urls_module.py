from typing import Optional
from datetime import date, datetime, timezone
import math

#Other
async def qp_select_list(q: Optional[str] = None, page: int = 1, limit: int = 100, nested: bool = False, entity_iin: str = ''):
    return {"q": q, "page": page, "limit": limit, 'nested': nested, 'entity_iin': entity_iin}

async def paginator(page: int = 1, limit: int = 100):
    return {"page": page, "limit": limit}

async def qp_select_one(q: Optional[str] = None, nested: bool = False):
    return {"q": q, 'nested': nested}

async def qp_update(q: Optional[str] = None, nested: bool = False):
    return {"q": q, 'nested': nested}

async def qp_insert(q: Optional[str] = None, nested: bool = False):
    return {"q": q, 'nested': nested}

def correct_date(date_value):
    if type(date_value) is str and date_value == 'None' or date_value == '': 
        return datetime.now(timezone.utc)
    elif type(date_value) is date or type(date_value) is date:
        return date_value
    else:
        return datetime.strptime(date_value, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    if type(date_value) is str and date_value == 'None' or date_value == '':  
        return datetime.now(timezone.utc)
    return datetime.strptime(date_value, '%Y-%m-%d').replace(tzinfo=timezone.utc)

def correct_datetime(date_value):
    if type(date_value) is str and len(date_value)==10:
        return datetime.strptime(date_value, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    elif type(date_value) is str and len(date_value)>10:
        return datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=timezone.utc) 
    elif type(date_value) is str and date_value == 'None' or date_value == '': 
        return datetime.now(timezone.utc)
    else:
        return date_value

async def paginator_execute(qp_select_list: dict, items_count: int):
    # количество запрошенный элементов - qp_select_list['limit']
    # запрашеваемая страница - qp_select_list['page']
    # общее количество записей в базе - items_count
    qp_select_list['pages'] = math.ceil(items_count/qp_select_list['limit'])

    if qp_select_list['page'] < 1:
        qp_select_list['page'] = 1

    if(qp_select_list['page'] > qp_select_list['pages']):
        qp_select_list['page'] = qp_select_list['pages']

    qp_select_list['has_previous'] = False if qp_select_list['page']==1 else True
    qp_select_list['has_next'] = False if qp_select_list['page']==qp_select_list['pages'] else True
    qp_select_list['skip'] = (qp_select_list['page']-1) * qp_select_list['limit']

    return qp_select_list
            
        
    
 

