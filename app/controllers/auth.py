from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.services.auth import login_for_access_token
from app.dependencies.database import db_dependency
from app.schemas.auth import Token

auth_router = APIRouter(prefix='/auth', tags=['auth'])
templates = Jinja2Templates(directory="app/view")

@auth_router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@auth_router.get("/logout")
def logout():
    response = RedirectResponse(url="/auth/login", status_code=303)
    response.delete_cookie("access_token")  
    return response

@auth_router.post("/token", response_model=Token)
def login_for_access_token_handler(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    return login_for_access_token(response, form_data, db)