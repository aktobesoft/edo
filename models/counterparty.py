
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date
from core.db import Base, metadata
from sqlalchemy.orm import relationship

class Сounterparty(Base):
    __tablename__ = "сounterparty"

    id = Column(Integer, primary_key=True, autoincrement=True) 
    name = Column(String(150), nullable=False)
    iin = Column(String(12), nullable=False, index=True, unique=True)
    address = Column(String(350))
    comment = Column(String(350))
    contact = Column(String(150))
    type_id = Column(Integer, ForeignKey('business_type.id', ondelete="CASCADE"))
    type = relationship("BusinessType")
    end_date = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    user = relationship("User")

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.name, self.iin)
