from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import MEDIUMTEXT 
from excerpts.database import Base

class Pages(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    contents = Column(MEDIUMTEXT)

    def __init__(self, contents="none"):
        self.contents = contents 

    def __repr__(self):
        return '<Contents %r>' % (self.contents)
