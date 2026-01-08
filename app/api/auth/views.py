from fastapi import APIRouter
from app.db.dependencies import SessionDep
from .schemas import UserLoginSchema, UserCreate, JWTToken
from .dependencies import TokenDep
from .utils import decode_jwt
from .service import UserService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register")
async def register(
    session: SessionDep,
    user_schema: UserCreate,
):
    user = await UserService.register_new_user(
        session,
        user_schema,
    )

    return user


@auth_router.post("/login")
async def login(
    session: SessionDep,
    user: UserLoginSchema,
) -> JWTToken:
    token = await UserService.login(session, user)
    return token


@auth_router.get("/me")
async def me(
    access_token: TokenDep,
):
    payload = decode_jwt(token=access_token)

    return payload
