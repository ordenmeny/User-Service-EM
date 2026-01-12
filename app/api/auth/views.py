from fastapi import APIRouter
from app.db.dependencies import SessionDep
from .schemas import UserLoginSchema, UserCreate, JWTToken, UserRead
from .dependencies import TokenDep
from .service import UserService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register")
async def register(
    session: SessionDep,
    user_schema: UserCreate,
):
    return await UserService.register_new_user(
        session,
        user_schema,
    )


@auth_router.post("/login")
async def login(
    session: SessionDep,
    user: UserLoginSchema,
) -> JWTToken:
    return await UserService.login(session, user)


@auth_router.get(
    "/me",
    response_model=UserRead,
)
async def me(
    session: SessionDep,
    access_token: TokenDep,
):
    return await UserService.get_user_by_token(
        session,
        access_token,
    )
