from db import DB
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Thune(Base):
    __tablename__ = "thunes"

    owner = Column(String(32), primary_key=True)
    amount = Column(Integer)


Base.metadata.create_all(DB().engine)
