from pydantic import BaseModel
from schemas.user import UserOut
from typing import List, Any
from datetime import date

class EntityOut(BaseModel):
    name: str
    iin: str
    address: str
    comment: str
    director: str
    director_phone: str
    administrator: str
    administrator_phone: str
    token: str
    startDate: date
    type: str
    user: UserOut
    
    class Config:
        orm_mode = True