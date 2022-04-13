from typing import Optional
from datetime import date, datetime

async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

def correct_date(date_value):
    if type(date_value) is str and date_value == 'None' or date_value == '':  
        return datetime.now()
    return datetime.strptime(date_value, '%Y-%m-%d')
