from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from core.db import Base, metadata

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
