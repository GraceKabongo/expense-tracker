from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from bcrypt import checkpw
from sqlmodel import select
from models.userModel import User
from uuid import UUID
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from models.tokenModel import TokenData
from services.db import user_session
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(password, hashed_password):
    return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_user(session, id: UUID):
    try:
        with session:
            statement = select(User).where(User.id == id)
            user = session.exec(statement=statement).first()
            if user :
               return user

    except Exception as e:
        print(e)


def authenticate_user(session, email: str, password: str):
    try:
        with session:
            statement = select(User).where(User.email == email)
            user = session.exec(statement=statement).first()
            if user and verify_password(password, user.password):
               return user
        
            if not user or not verify_password(password, user.password):
                return False
        
    except Exception as e:
        print(e)

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):


    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=UUID(user_id))
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(user_session, id=token_data.id)
    if user is None:
        raise credentials_exception
    return user

