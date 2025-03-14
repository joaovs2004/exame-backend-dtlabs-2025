from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select

from app.services.auth_services import authenticate_user, create_access_token, get_password_hash
from app.db import session
from app.db.models import User
from app.models.auth_models import NewUser, Token

router = APIRouter()

@router.post("/auth/register", tags=["auth"])
async def register_user(new_user: NewUser, session: session.SessionDep):
    """
    Endpoint for user creation. After the user is created you can use the login endpoint to obtain a jwt token
    """
    user_in_db = session.exec(select(User).where(User.name == new_user.name)).first()

    if user_in_db:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user.password = get_password_hash(new_user.password)
    session.add(User(name=new_user.name, password=new_user.password))
    session.commit()
    return {"message": "User created"}

@router.post("/auth/login", tags=["auth"])
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: session.SessionDep
):
    """
        Endpoint to get the token needed for authentication
    """
    user = authenticate_user(session, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.name})

    return Token(access_token=access_token, token_type="bearer")