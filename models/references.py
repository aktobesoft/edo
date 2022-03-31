from enum import unique
from sqlalchemy import Column, String, Integer, Table, DateTime, Boolean, MetaData, ForeignKey, Date
from sqlalchemy.orm import relationship
from core.db import Base, metadata

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class BusinessType(Base):
    __tablename__ = "business_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True)
    full_name = Column(String(360))

    def __repr__(self) -> str:
        return self.name
        
class DocumentType(Base):
    __tablename__ = "document_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False, unique=True)
    description = Column(String(350), nullable=False)

    def __repr__(self) -> str:
        return self.description


class Entity(Base):
    __tablename__ = "entity"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    iin = Column(String(12), nullable=False, index=True, unique=True)
    address = Column(String(350), nullable=True)
    comment = Column(String(350), nullable=True)
    director = Column(String(150), nullable=True)
    director_phone = Column(String(20), nullable=True)
    administrator = Column(String(150), nullable=True)
    administrator_phone = Column(String(20), nullable=True)
    token = Column(String(64), nullable=True)
    startDate = Column(Date, nullable=True)
    endDate = Column(Date, nullable=True)
    type_id = Column(Integer, ForeignKey('business_type.id', ondelete="CASCADE"), nullable=True)
    type = relationship("BusinessType")
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    user = relationship("User")

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.name, self.iin)

class Employee(Base):
    __tablename__ = "employee"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    date_of_birth = Column(Date, nullable=True)
    name = Column(String(150), nullable=False)
    description = Column(String(350), nullable=True)
    entity_id = Column(Integer, ForeignKey('entity.id', ondelete="CASCADE"), nullable=False)
    entity = relationship("Entity")
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    user = relationship("User")

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.name, self.email)

class EmployeeActivity(Base):
    __tablename__ = "employee_activity"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, unique=True)
    last_activity = Column(DateTime(timezone=True))
    employee_id = Column(Integer, ForeignKey('employee.id', ondelete="CASCADE"))
    employee = relationship("Employee")
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    user = relationship("User")

    def __repr__(self) -> str:
        return '<{0} - {1}>'.format(self.employee, self.last_activity)

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
    endDate = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    user = relationship("User")

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.name, self.iin)

class Notes(Base):
    __tablename__ = "notes"
    id  = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    completed = Column(Boolean)

    def __repr__(self) -> str:
        return '<{0} ({1})>'.format(self.id, self.text)