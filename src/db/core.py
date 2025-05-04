from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# 1. Try to get DATABASE_URL directly
#DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = ""
print(f"Getting DATABASE_URL from .env: {DATABASE_URL}")
# 2. If not found, build it from individual AWS credentials
if not DATABASE_URL:
    AWS_PG_HOST = os.getenv("AWS_PG_HOST")
    AWS_PG_PORT = os.getenv("AWS_PG_PORT", "5432")
    AWS_PG_USER = os.getenv("AWS_PG_USER", "postgres")
    AWS_PG_PASSWORD = os.getenv("AWS_PG_PASSWORD", "postgres")
    AWS_PG_DATABASE = os.getenv("AWS_PG_DATABASE", "main_service")

    if AWS_PG_HOST and AWS_PG_PASSWORD:
        DATABASE_URL = f"postgresql://{AWS_PG_USER}:{AWS_PG_PASSWORD}@{AWS_PG_HOST}:{AWS_PG_PORT}/{AWS_PG_DATABASE}"
        print(f"Using constructed AWS DATABASE_URL: {DATABASE_URL}")
    else:
        # Fallback to local dev DB
        DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/main_service"
        print(f"Using local dev DATABASE_URL: {DATABASE_URL}")
# 3. Setup SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 4. Dependency for FastAPI
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbSession = Annotated[Session, Depends(get_db)]
