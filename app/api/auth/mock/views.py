from fastapi import APIRouter, Response
from app.api.auth.schemas import UserCreate, UserRead
from app.api.auth.service import AuthService
from dataclasses import dataclass

mock_router = APIRouter(prefix="/api/v1/auth/mock", tags=["mock"])


@dataclass(frozen=True, slots=True)
class UserMock:
    id: int
    first_name: str
    last_name: str
    patronymic: str
    email: str
    password: str  # hashed
    is_admin: bool
    is_active: bool


@mock_router.post("/register")
async def mock_auth(
    user_sheme: UserCreate,
    response: Response,
):
    user = UserMock(
        id=1,
        first_name=user_sheme.first_name,
        last_name=user_sheme.last_name,
        patronymic=user_sheme.patronymic,
        email=user_sheme.email,
        password=user_sheme.password,
        is_admin=False,
        is_active=True,
    )

    return {
        "access_token": await AuthService.create_token(user, response),
        "user": UserRead.model_validate(user),
    }
