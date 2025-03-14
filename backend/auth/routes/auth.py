from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from models.tokenModel import Token
from auth.authentication import authenticate_user, create_access_token
from services.db import user_session
import os

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)



class OAuth2EmailRequestForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        email: str = Form(...),  # Replace username with email
        password: str = Form(...),
        scope: str = Form(""),
        client_id: str | None = Form(None),
        client_secret: str | None = Form(None),
    ):
        self.username = email  # Trick FastAPI to think email is username
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret



@router.post("/login")
async def login_for_access_token(form_data: Annotated[OAuth2EmailRequestForm, Depends()],) -> Token:
    try:
        user = authenticate_user(user_session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(
            minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))  # Default to 15 minutes
        )
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

    except Exception as e:
        print("Login Error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error, please try again later",
        )
    
    return Token(access_token=access_token, token_type="bearer")