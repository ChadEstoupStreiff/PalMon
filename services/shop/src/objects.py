from db import DB
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Thune(Base):
    __tablename__ = "thunes"

    owner = Column(String(32), primary_key=True)
    amount = Column(Integer)


Base.metadata.create_all(DB().engine)
