from typing import Optional
from datetime import date, datetime, timezone
import math

#Other
async def query_parameters_list(q: Optional[str] = '', page: int = 1, limit: int = 100, nested: bool = False):
    return {"q": q, "page": page, "limit": limit, 'nested': nested}

async def paginator(page: int = 1, limit: int = 100):
    return {"page": page, "limit": limit}

async def approval_parameters(include_approve_route: bool = False):
    return {"include_approve_route": include_approve_route}

async def query_parameters(q: Optional[str] = '', nested: bool = False):
    return {"q": q, 'nested': nested}

def correct_date(date_value):
    if type(date_value) is str and date_value == 'None' or date_value == '': 
        return datetime.now(timezone.utc)
    elif type(date_value) is date or type(date_value) is date:
        return date_value
    else:
        return datetime.strptime(date_value, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    # if type(date_value) is str and date_value == 'None' or date_value == '':  
    #     return datetime.now(timezone.utc)
    # return datetime.strptime(date_value, '%Y-%m-%d').replace(tzinfo=timezone.utc)

def correct_datetime(date_value):
    if type(date_value) is str and len(date_value)==10:
        return datetime.strptime(date_value, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    elif type(date_value) is str and len(date_value)>10:
        return datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=timezone.utc) 
    elif type(date_value) is str and date_value == 'None' or date_value == '': 
        return datetime.now(timezone.utc)
    else:
        return date_value

async def paginator_execute(parameters: dict, items_count: int):
    # количество запрошенный элементов - parameters['limit']
    # запрашеваемая страница - parameters['page']
    # общее количество записей в базе - items_count
    parameters['pages'] = math.ceil(items_count/parameters['limit'])

    if parameters['page'] < 1:
        parameters['page'] = 1

    if(parameters['page'] > parameters['pages']):
        parameters['page'] = parameters['pages']

    parameters['has_previous'] = False if parameters['page']==1 else True
    parameters['has_next'] = False if parameters['page']==parameters['pages'] else True
    parameters['skip'] = (parameters['page']-1) * parameters['limit'] if parameters['page'] > 1 else 0

def is_need_filter(key: str = 'entity_iin', parameters: dict = {}):
    if ('current_user' in parameters and parameters['current_user']['is_admin']):
        return False
    if (key in parameters and (parameters[key] != '' and parameters[key] != [])):
        return True
    return True


            
        
    
 

