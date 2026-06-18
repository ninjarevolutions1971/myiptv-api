from fastapi import FastAPI
from pydantic import BaseModel
from database import engine, SessionLocal
from models import Base, User, Playlist

Base.metadata.create_all(bind=engine)

app = FastAPI()


class UserCreate(BaseModel):
    username: str
    email: str
    
class PlaylistCreate(BaseModel):
    name: str
    url: str

@app.get("/")
def root():
    return {"message": "MyIPTV API Online"}


@app.post("/users")
def create_user(user: UserCreate):
    db = SessionLocal()

    new_user = User(
        username=user.username,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }


@app.get("/users")
def get_users():
    db = SessionLocal()

    users = db.query(User).all()

    result = [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email
        }
        for u in users
    ]

    db.close()

    return result
@app.post("/playlists")
def create_playlist(playlist: PlaylistCreate):
    db = SessionLocal()

    new_playlist = Playlist(
        name=playlist.name,
        url=playlist.url
    )

    db.add(new_playlist)
    db.commit()
    db.refresh(new_playlist)

    db.close()

    return {
        "id": new_playlist.id,
        "name": new_playlist.name,
        "url": new_playlist.url
    }


@app.get("/playlists")
def get_playlists():
    db = SessionLocal()

    playlists = db.query(Playlist).all()

    result = [
        {
            "id": p.id,
            "name": p.name,
            "url": p.url
        }
        for p in playlists
    ]

    db.close()

    return result
