from fastapi import APIRouter

from app.db import session
from app.models.servers_models import NewServer
from app.services.servers_services import create_new_server

router = APIRouter()

@router.post("/servers", tags=["servers"])
def create_server(new_server: NewServer, session: session.SessionDep):
    create_new_server(new_server, session)
    return {"message": "Server created"}
