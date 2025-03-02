from typing import Annotated
from fastapi import APIRouter, Depends

from app.db import session
from app.db.models import User
from app.models.servers_models import NewServer
from app.services.auth_services import get_current_user
from app.services.servers_services import create_new_server

router = APIRouter()

@router.post("/servers", tags=["servers"])
async def create_server(
    user: Annotated[User, Depends(get_current_user)],
    new_server: NewServer,
    session: session.SessionDep
    ):
    """
    Endpoint to create new servers. Authentication required
    """
    server_ulid = create_new_server(new_server, session)
    return {
        "server_name": new_server.name,
        "server_ulid": server_ulid
    }
