from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from core.db import Base, metadata

class Notes(Base):
    __tablename__ = "notes"
    id  = Column(Integer, primary_key = True, autoincrement = True)
    text = Column(String)
    completed = Column(Boolean)

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.id, self.text)

class NotesOut(BaseModel):
    id: int
    text: str
    completed: bool

class UserOut(BaseModel):
    id: int
    email: str
    is_active: bool

    class Config:
        orm_mode = True