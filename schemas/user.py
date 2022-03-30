from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    email: str
    is_active: bool

    class Config:
        orm_mode = True