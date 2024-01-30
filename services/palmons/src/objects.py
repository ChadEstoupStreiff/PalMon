from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import DB

Base = declarative_base()

class Palmon(Base):
    __tablename__ = 'palmons'

    id = Column(Integer, primary_key=True)
    type = Column(String(16))
    lvl = Column(Integer)
    hp = Column(Integer)
    stat_hp = Column(Integer)
    stat_dmg = Column(Integer)
    stat_def = Column(Integer)
    stat_spd = Column(Integer)

class BagSlot(Base):
    __tablename__ = 'bags'

    owner = Column(String(32))
    palmon_id = Column(Integer, ForeignKey('palmons.id'), primary_key=True)

    palmon = relationship("Palmon")

class StorageSlot(Base):
    __tablename__ = 'storages'

    owner = Column(String(32))
    palmon_id = Column(Integer, ForeignKey('palmons.id'), primary_key=True)
    
    palmon = relationship("Palmon")


Base.metadata.create_all(DB().engine)
