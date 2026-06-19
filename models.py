from sqlalchemy import Column, Integer, String, ForeignKey, Date
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)

    playlist_id = Column(Integer, ForeignKey("playlists.id"))
    expire_date = Column(Date)


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
