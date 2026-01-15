from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from app.db.dependencies import SessionDep
from .models import User
from .service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

TokenDep = Annotated[str, Depends(oauth2_scheme)]

FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


async def get_current_user(
    session: SessionDep,
    token: TokenDep,
) -> User:
    user = await UserService.get_user_by_token(session, token)
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def admin_required(session: SessionDep, token: TokenDep) -> None:
    user = await UserService.get_user_by_token(session, token)
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="for admin only",
        )


admin_required = Depends(admin_required)


# async def get_current_user(
#     session: SessionDep,
#     access_token: TokenDep
# ):
#     payload = decode_jwt(token=access_token)
#
#     user = await cls.user_dao.get_user_by_email(
#         session,
#         payload.get("email"),
#     )
#
#     if user is None:
#         raise HTTPException(status_code=401, detail="User not found, you need to login")
#
#     return user
