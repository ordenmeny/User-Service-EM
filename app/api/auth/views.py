from fastapi import APIRouter
from app.db.dependencies import SessionDep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/")
async def hello_users(session: SessionDep):
    return {"message": "Hello Users"}
