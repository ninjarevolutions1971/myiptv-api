from sqlalchemy import Column, Integer, String, Date
from database import Base
from datetime import date
from fastapi import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
from database import engine, SessionLocal
from models import Base, User, Playlist
import requests

Base.metadata.create_all(bind=engine)

app = FastAPI()


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    playlist_id: int
    expire_date: date
    
class PlaylistCreate(BaseModel):
    name: str
    url: str

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def root():
    return {"message": "MyIPTV API Online"}


@app.post("/users")
def create_user(user: UserCreate):
    db = SessionLocal()

    new_user = User(
    username=user.username,
    password=user.password,
    email=user.email,
    playlist_id=user.playlist_id,
    expire_date=user.expire_date
)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return {
    "id": new_user.id,
    "username": new_user.username,
    "password": new_user.password,
    "email": new_user.email,
    "playlist_id": new_user.playlist_id
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


@app.post("/login")
def login(user_data: LoginRequest):
    db = SessionLocal()

    user = db.query(User).filter(
        User.username == user_data.username,
        User.password == user_data.password
    ).first()

    if not user:
        db.close()
        return {"error": "Credenziali non valide"}

    if db_user.expire_date < date.today():
        db.close()
        raise HTTPException(
            status_code=403,
            detail="Abbonamento scaduto"
        )

    playlist = db.query(Playlist).filter(
        Playlist.id == user.playlist_id
    ).first()

    db.close()

    if not playlist:
        return {"error": "Playlist non trovata"}

    return {
        "username": user.username,
        "playlist": playlist.name,
        "url": playlist.url
    }

@app.get("/playlists/{playlist_id}/stats")
def playlist_stats(playlist_id: int):
    db = SessionLocal()

    playlist = db.query(Playlist).filter(
        Playlist.id == playlist_id
    ).first()

    db.close()

    if not playlist:
        return {"error": "Playlist non trovata"}

    try:
        response = requests.get(
            playlist.url,
            timeout=20
        )

        content = response.text

        channels = content.count("#EXTINF")

        return {
            "playlist_id": playlist.id,
            "name": playlist.name,
            "channels": channels
        }

    except Exception as e:
        return {
            "error": str(e)
        }
