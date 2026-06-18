from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
