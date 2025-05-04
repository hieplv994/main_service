from fastapi import FastAPI
from src.db.core import engine, Base
from .api import register_api_routes
from src.server_log import configure_logging, LogLevels

configure_logging(LogLevels.INFO)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
register_api_routes(app)