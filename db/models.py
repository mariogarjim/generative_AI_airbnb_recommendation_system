from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Date, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base  = declarative_base()

class Listing(Base):
    """Airbnb listings data table"""
    __tablename__ = 'listings'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    accommodates = Column(Integer)
    minimum_nights = Column(Integer)
    
    # Relationship with Calendar
    calendars = relationship("Calendar", back_populates="listing")

class Calendar(Base):
    """Airbnb availability calendar data table"""
    __tablename__ = 'calendar'
    
    listing_id = Column(Integer, ForeignKey('listings.id'), primary_key=True)
    date = Column(Date, primary_key=True)
    available = Column(Boolean)
    price = Column(Integer)
    
    # Foreign key constraint
    listing = relationship("Listing", back_populates="calendars")