from app.db import session
from app.db.models import Server
from app.models.servers_models import NewServer
import ulid

def create_new_server(new_server: NewServer, session: session.SessionDep):
    server_ulid = ulid.new().str

    session.add(Server(
        server_id=server_ulid,
        name=new_server.name,
    ))
    session.commit()