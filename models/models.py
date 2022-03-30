from enum import unique
from sqlalchemy import Column, String, Integer, Table, DateTime, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base, metadata

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
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
    endDate = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), index=True)
    user = relationship("User")

    def __repr__(self) -> str:
        return '{0} ({1})'.format(self.name, self.iin)
    

class Notes(Base):
    __tablename__ = "notes"
    id  = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    completed = Column(Boolean)

    def __repr__(self) -> str:
        return '{0} ({1})'.format(self.id, self.text)