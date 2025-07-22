from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.services.auth import login_for_access_token
from app.dependencies.database import db_dependency
from app.schemas.auth import Token

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.post("/token", response_model=Token)
def login_for_access_token_handler(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    return login_for_access_token(form_data, db)