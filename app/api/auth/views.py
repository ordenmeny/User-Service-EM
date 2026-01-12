from fastapi import APIRouter, Response
from app.db.dependencies import SessionDep
from .schemas import (
    UserLoginSchema,
    UserCreate,
    JWTToken,
    UserRead,
    UserUpdate,
    OAuthTokenResponse
)
from .dependencies import TokenDep, FormDep
from .service import UserService

auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


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


@auth_router.post("/token", response_model=OAuthTokenResponse)
async def login_token(
    session: SessionDep,
    form: FormDep,
) -> JWTToken:
    user = UserLoginSchema(
        email=form.username,
        password=form.password,
    )
    token = await UserService.login(session, user)

    response = OAuthTokenResponse(
        access_token=token.token,
        token_type="bearer"
    )

    return response


@auth_router.get(
    "/me",
    response_model=UserRead,
)
async def get_current_user(
    session: SessionDep,
    access_token: TokenDep,
):
    return await UserService.get_user_by_token(
        session,
        access_token,
    )


@auth_router.patch(
    "/me",
    response_model=UserRead,
)
async def update_current_user(
    session: SessionDep,
    access_token: TokenDep,
    user_schema: UserUpdate,
):
    return await UserService.update_user_by_token(
        session,
        access_token,
        user_schema,
    )


@auth_router.post("/logout")
async def logout():
    # Удаление refresh_token из httponly-кук.
    return Response(status_code=200)
