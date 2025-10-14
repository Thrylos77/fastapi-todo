from typing import Annotated
from uuid import UUID, uuid4
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models.user import User
from . import model
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jwt import PyJWTError
from datetime import datetime, timedelta, timezone
from app.core.exceptions import AuthenticationError

from dotenv import load_dotenv

import logging
import jwt
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
if not SECRET_KEY or not ALGORITHM or not ACCESS_TOKEN_EXPIRE_MINUTES:
    raise ValueError("SECRET_KEY, ALGORITHM, and ACCESS_TOKEN_EXPIRE_MINUTES must be set in environment variables.")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

# CryptContext : argon2 firt, bcrypt for fallback (verify old hashes)
pwd_context = CryptContext(
    schemes=['argon2', 'bcrypt'], 
    deprecated='auto'   # mark older schemes as deprecated so passlib can suggest upgrade
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(db: Session, identifier: str, password: str) -> User | bool:
    user = db.query(User).filter((User.username == identifier) | (User.email == identifier)).first()
    if not user or not verify_password(password, user.hashed_password):
        logging.warning(f"Authentication failed for user with this identifier : {identifier} ")
        return False
    return user

def create_access_token(email: str, username: str, user_id: UUID, expires_delta: timedelta) -> str:
    encode = {
        'sub': email,
        'username': username,
        'id': str(user_id),
        'exp': datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> model.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        token_data = model.TokenData(user_id=user_id)
    except PyJWTError as e:
        logging.warning(f"Token verification failed: {str(e)}")
        raise AuthenticationError()
    return token_data

def register_user(db: Session, user: model.RegisterUserRequest) -> None:
    try:
        hashed_password = get_hashed_password(user.password)
        db_user = User(
            id=uuid4(),
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        logging.error(f"Error registering user: {user.email}. Error: {str(e)}")
        db.rollback()
        raise
    return db_user

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> model.TokenData:
    return verify_token(token)

CurrentUser = Annotated[model.TokenData, Depends(get_current_user)]

def login_for_access_token(db: Session, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> model.Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise AuthenticationError()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        user.email,
        user.username,
        user.id,
        access_token_expires
    )
    return model.Token(access_token=token, token_type="bearer")