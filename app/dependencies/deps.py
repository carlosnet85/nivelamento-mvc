from fastapi import Depends, HTTPException
from starlette import status

from app.core.auth import decode_access_token
from app.database.session import SessionLocal
from app.core.security import oauth2_scheme

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token) 
    
    user_email = payload.get("sub")
    user_id = payload.get("user_id") 

    if user_email is None or user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"email": user_email, "id": user_id}

