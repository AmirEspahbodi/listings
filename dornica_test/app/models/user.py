import enum

from sqlalchemy import Column, String, Date, Enum, Integer, TIMESTAMP
from sqlalchemy.orm import relationship

from app.db.database import Base

class GenderEnum(enum.Enum):
    MAIL = 'MAIL'
    FEMAIL = 'FEMAIL'
    NOT_SPECIFIED = 'NOT_SPECIFIED'

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    full_name = Column(String, nullable=True)
    email = Column(String, nullable=False) #, unique=True)
    password = Column(String, nullable=False)
    gender = Column(Enum(GenderEnum), default=GenderEnum.NOT_SPECIFIED,)
    BoD = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
    
    listings = relationship('Listing', back_populates='owner')
