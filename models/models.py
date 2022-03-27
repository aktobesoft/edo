from enum import unique
from turtle import title
from sqlalchemy import Column, String, Integer, Text, DateTime
from core.db import Base

class DocumentType(Base):
    __tablename__ = "documentType"

    name = Column(String(150), primary_key=True, nullable=False)
    description = Column(String(350), nullable=False)

    def __repr__(self) -> str:
        return self.description


class Entity(Base):
    __tablename__ = "entity"

    name = Column(String(150), nullable=False)
    iin = Column(String(12), primary_key=True, nullable=False)
    address = Column(String(350))
    comment = Column(String(350))
    director = Column(String(150))
    director_phone = Column(String(20))
    administrator = Column(String(150))
    administrator_phone = Column(String(20))
    token = Column(String(64))
    startDate = Column(DateTime)
    type = Column(String(20))
    endDate = Column(String(20))
    user = Column(String(20))

    def __repr__(self) -> str:
        return '{0} ({1})'.format(self.name, self.iin)
    