from typing import Optional
from datetime import date, datetime, timezone

from sqlalchemy import false

async def qp_select_list(q: Optional[str] = None, skip: int = 0, limit: int = 100, nested: bool = False, optional: bool = False):
    return {"q": q, "skip": skip, "limit": limit, 'nested': nested, 'optional': optional}

async def qp_select_one(q: Optional[str] = None, nested: bool = False):
    return {"q": q, 'nested': nested}

async def qp_update(q: Optional[str] = None, nested: bool = False):
    return {"q": q, 'nested': nested}

async def qp_insert(q: Optional[str] = None, nested: bool = False):
    return {"q": q, 'nested': nested}

def correct_datetime(date_value):
    if type(date_value) is str and date_value == 'None' or date_value == '':  
        return datetime.now(timezone.utc)
    return datetime.strptime(date_value, '%Y-%m-%d').replace(tzinfo=timezone.utc)

def correct_datetime(date_value):
    if type(date_value) is str and date_value == 'None' or date_value == '': 
        return datetime.now(timezone.utc)
    elif type(date_value) is date or type(date_value) is datetime:
        return date_value
    else:
        return datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=timezone.utc)
