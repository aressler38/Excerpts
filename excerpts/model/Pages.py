from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import MEDIUMTEXT, VARCHAR
from excerpts.database import Base

class Pages(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    contents = Column(MEDIUMTEXT)
    title = Column(VARCHAR(1024))

    def __init__(self, contents="none", title="null"):
        self.contents = contents 
        self.title = title

    def __repr__(self):
        return '<Contents %r>' % (self.contents)
