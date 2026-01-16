from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends
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
