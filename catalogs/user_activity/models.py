
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from core.db import Base

class UserActivity(Base):
    __tablename__ = "user_activity"
    
    id = Column(Integer, primary_key = True, autoincrement = True)
    device_token = Column(String)
    last_activity = Column(DateTime(timezone=True))
    action = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'), index = True)
    user = relationship("User")

    def __repr__(self) -> str:
        return '<{0} - {1}>'.format(self.user_id, self.last_activity)
