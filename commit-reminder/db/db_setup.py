import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(250), nullable=False)
    gh_username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    avatar_url = Column(String(250))

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
print "DB created!"
