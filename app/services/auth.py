from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from starlette import status

from app.models.customer import Customer
from app.core.auth import create_access_token, verify_password
from app.dependencies.database import db_dependency
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(Customer).filter(Customer.email == email).first()
    if not user:
        return False
    if not verify_password(password, str(user.password)):
        return False
    return user

def login_for_access_token(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token(
        data={"sub": str(user.email), "user_id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    

    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        max_age=3600,  
        secure=False,
        samesite="lax"
    )
    

    return {"access_token": token, "token_type": "bearer"}

