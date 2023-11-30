from sqlalchemy import Column, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "image"

    teamname = Column(VARCHAR, nullable=False, primary_key=True)
    username = Column(VARCHAR, nullable=False, primary_key=True)
    image = Column(VARCHAR, nullable=False)

    def __str__(s):
        return ("teamname:" +s.teamname + " username:" + s.username)


class Room(Base):
    __tablename__ = "room"

    teamname = Column(VARCHAR, nullable=False, autoincrement=True, primary_key=True)
    password = Column(VARCHAR, nullable=False)


    def __str__(s):
        return ("teamname:" +s.teamname + " username:" + s.password)
