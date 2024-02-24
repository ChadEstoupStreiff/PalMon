from db import DB
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Egg(Base):
    __tablename__ = "eggs"

    owner = Column(String(32), primary_key=True)
    amount = Column(Integer)


class Incubator(Base):
    __tablename__ = "incubators"

    incubator_id = Column(Integer, primary_key=True, autoincrement=True)
    owner = Column(String(32), primary_key=True)
    occupied = Column(Boolean)
    hatch_date = Column(DateTime)


Base.metadata.create_all(DB().engine)
