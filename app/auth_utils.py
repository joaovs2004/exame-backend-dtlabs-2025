import os
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from sqlmodel import select

from app.db import session
from app.db.models import User

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(hours=5)

    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def authenticate_user(session: session.SessionDep, username: str, password: str):
    user = session.exec(select(User).where(User.name == username)).first()

    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user