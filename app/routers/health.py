from typing import Annotated
from fastapi import APIRouter, Depends

from app.db import session
from app.db.models import User
from app.services.auth_services import get_current_user
from app.services.health_services import get_server_health_by_id, get_all_health

router = APIRouter()

@router.get("/health/all", tags=["health"])
def get_all_server_health(user: Annotated[User, Depends(get_current_user)], session: session.SessionDep):
    response = get_all_health(session)
    return response

@router.get("/health/{server_id}", tags=["health"])
def get_server_health(server_id: str, user: Annotated[User, Depends(get_current_user)], session: session.SessionDep):
    response = get_server_health_by_id(server_id, session)
    return response
