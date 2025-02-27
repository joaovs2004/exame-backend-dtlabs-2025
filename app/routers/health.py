from fastapi import APIRouter

router = APIRouter()

@router.get("/health/all", tags=["health"])
def get_all_server_health():
    return {"message": "ok"}

@router.get("/health/{server_id}", tags=["health"])
def get_server_health(server_id: int):
    return {"message": "ok"}
