import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


load_dotenv()


DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set in the environment."
    )


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    Provide a database session and ensure it is
    closed after use.
    """

    db: Session = SessionLocal()

    try:
        yield db

    finally:
        db.close()
