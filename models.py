import os
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from datetime import datetime

# path for database file
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_string = "sqlite:///"+os.path.join(BASE_DIR, 'site.db')

# setting up engine
engine = create_engine(connection_string, echo=True)

# creating session object
Session = sessionmaker()

# base class for models
Base = declarative_base()

# Members table schema
class Member(Base):
    __tablename__ = 'Members'
    id = Column(Integer(), primary_key=True)
    name = Column(String(25), unique=True, nullable=False)
    date_created = Column(DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f'<Member name={self.name} date_created={self.date_created}>'

# test_member = Member(name='Wumpus')
# print(test_member)
