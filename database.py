from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://myiptv_user:VeKf23sPA6s1ccrgLg7I3FJijkG7FDzf@dpg-d8q1u8r6sc1c73b0g6cg-a.ohio-postgres.render.com/myiptv"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()