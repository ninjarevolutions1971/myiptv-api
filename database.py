from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://myiptv_user:KtKM4xLJjmzZPakocr8EieyuzHKZ4ddB@dpg-d8q8npojs32c738td8j0-a/myiptv_8v0t"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "sslmode": "require"
    },
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
