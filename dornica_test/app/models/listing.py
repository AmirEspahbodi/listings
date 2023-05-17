import enum
from sqlalchemy import Column, String, DateTime, Enum, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class ListingTypeEnum(enum.Enum):
    HOUSE = 'HOUSE'
    APARTMENT = 'APARTMENT'


class Listing(Base):
    __tablename__ = 'listings'
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(ListingTypeEnum), nullable=False)
    available_now = Column(Boolean, default=True)
    address = Column(String, nullable=False) #, unique=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship('User', back_populates='listings')
