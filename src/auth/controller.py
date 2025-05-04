from typing import Annotated
from fastapi import APIRouter, Depends, Request
from starlette import status
from . import model, service
from fastapi.security import OAuth2PasswordRequestForm
from src.db.core import DbSession
from src.rate_limiting import limiter

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register_user(request: Request, db: DbSession, user: model.RegisterUserRequest):
    service.register_user(db, user)
    
@router.post("/token", response_model=model.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    return service.login_for_access_token(db, form_data)