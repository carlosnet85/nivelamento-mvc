from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette import status

from app.core.config import SECRET_KEY, ALGORITHM

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt_context.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)

