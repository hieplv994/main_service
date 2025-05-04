from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import uuid4, UUID
from fastapi import Depends
from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
from sqlalchemy.orm import Session
from src.entities.user import User
from . import model
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str) -> User | bool:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        logging.warning(f"Failed authentication for user {email}")
        return False
    return user

def create_access_token(email: str, user_id: UUID,   expires_delta: timedelta = None) -> str:
    encode = {"sub": email, "id": str(user_id), 'exp': datetime.now(timezone.utc) + expires_delta}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> model.TokenData:
    try:
        decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = decode.get("id")
        return model.TokenData(user_id=user_id)
    except PyJWTError as e:
        logging.warning(f"Failed to decode token: {str(e)}")
        return model.TokenData(user_id=None)
    

def register_user(db: Session, user: model.RegisterUserRequest) -> User | bool:
    try:
        db_user = User(email=user.email, first_name=user.first_name, last_name=user.last_name, password_hash=get_password_hash(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        logging.error(f"Failed to register user: {str(e)}")
        return False
    
def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> model.TokenData:
    return verify_token(token)

CurrentUser = Annotated[model.TokenData, Depends(get_current_user)]

def login_for_access_token(db: Session, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> model.Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise Exception("Invalid credentials")
    token = create_access_token(user.email, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return model.Token(access_token=token, token_type="bearer")