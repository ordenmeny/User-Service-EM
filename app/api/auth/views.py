from fastapi import APIRouter, Response, status, Cookie
from fastapi.responses import ORJSONResponse
from .schemas import (
    UserLoginSchema,
    UserCreate,
    JWTToken,
    UserRead,
    UserUpdate,
    OAuthTokenResponse,
)
from .dependencies import TokenDep, FormDep
from .service import UserService, AuthService
from .permissions import admin_required
from .dependencies import CurrentUserDep
from app.db.dependencies import SessionDep
from .utils import encode_jwt, decode_jwt

auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@auth_router.post("/register")
async def register(
    session: SessionDep,
    user_schema: UserCreate,
    response: Response,
):
    return await UserService.register_new_user(
        session,
        user_schema,
        response,
    )


@auth_router.post("/login")
async def login(
    session: SessionDep, user: UserLoginSchema, response: Response
) -> JWTToken:
    return await UserService.login(session, user, response)


@auth_router.post("/token", response_model=OAuthTokenResponse)
async def login_token(
    form: FormDep,
) -> JWTToken:
    user = UserLoginSchema(
        email=form.username,
        password=form.password,
    )
    token = await UserService.login(user)

    response = OAuthTokenResponse(access_token=token.token, token_type="bearer")

    return response


@auth_router.get(
    "/me",
    response_model=UserRead,
)
async def get_current_user(
    current_user: CurrentUserDep,
):
    return current_user


@auth_router.patch(
    "/me",
    response_model=UserRead,
)
async def update_current_user(
    session: SessionDep,
    user_schema: UserUpdate,
    current_user: CurrentUserDep,
):
    return await UserService.update_user_by_token(
        session,
        current_user,
        user_schema,
    )


@auth_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="refresh_token", path="/")
    response.status_code = status.HTTP_200_OK
    return {"detail": "logout"}


@auth_router.delete("/me")
async def soft_delete_account(
    session: SessionDep,
    access_token: TokenDep,
):
    await logout()

    await UserService.soft_delete_user_by_token(session, access_token)

    return ORJSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": "user soft deleted"}
    )


@auth_router.post("/refresh")
async def refresh_access_token(
    session: SessionDep,
    response: Response,
    refresh_token: str = Cookie(default=None),
) -> JWTToken:
    payload = decode_jwt(refresh_token)

    user = await UserService.get_user_by_email(
        session,
        payload.get("email"),
    )

    token = await AuthService.create_token(user, response)

    return token


@auth_router.get("/for-admin", dependencies=[admin_required])
async def for_admin_only():
    return {"message": "this content for admin only, you are an admin."}
