from sqlalchemy.orm import sessionmaker

from backend.database.database import engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)