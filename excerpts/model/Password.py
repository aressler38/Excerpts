from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mysql import TEXT 
from excerpts.database import Base

class Password(Base):
    __tablename__ = 'password'
    id = Column(Integer, primary_key=True)
    password = Column(TEXT)

    def __init__(self, password=None):
        self.password = contents 

    def __repr__(self):
        return None
