from fastapi import HTTPException, status, Response
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import (
    UserCreate,
    UserRead,
    JWTToken,
    UserUpdate,
    UserLoginSchema,
)
from .utils import encode_jwt, check_password, decode_jwt
from .dao import UserDAO
from .models import User
from .custom_types import JWTTokenStr
from app.core.custom_exceptions import InvalidCredentialsError
from .base_dao import BaseUserDAO
from typing import Type
from app.core.config import settings


class AuthService:
    @classmethod
    async def create_token(cls, user_db: User, response: Response) -> JWTToken:
        payload = {
            "sub": str(user_db.id),
            "email": user_db.email,
            "is_active": user_db.is_active,
        }

        refresh_token = encode_jwt(
            payload, exp=settings.auth_jwt.refresh_token_lifetime
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=int(settings.auth_jwt.refresh_token_lifetime.total_seconds()),
            path="/",
        )

        return JWTToken(
            token=encode_jwt(payload),
            token_type="bearer",
        )


class UserService:
    user_dao: Type[BaseUserDAO[User, UserUpdate]] = UserDAO

    @classmethod
    async def login(
        cls,
        session: AsyncSession,
        user: UserLoginSchema,
        response: Response,
    ) -> JWTToken:
        user_db = await cls.user_dao.get_user_by_email(session, user.email)

        if user_db is None:
            raise InvalidCredentialsError()

        input_password = user.password
        hashed_password = str(user_db.password)

        if not check_password(input_password, hashed_password):
            raise InvalidCredentialsError()

        access_token = await AuthService.create_token(user_db, response)

        return access_token

    @classmethod
    async def register_new_user(
        cls, session: AsyncSession, user_schema: UserCreate, response: Response
    ):

        user = user_schema.model_dump(exclude={"password2"})

        user_exists = await cls.user_dao.get_user_by_email(
            session,
            user["email"],
        )
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )

        user_db = await cls.user_dao.add_to_db(session, user)

        access_token = await AuthService.create_token(user_db, response)

        return {
            "credentials": access_token,
            "user": UserRead.model_validate(user_db),
        }

    @classmethod
    async def get_user_by_token(
        cls,
        session: AsyncSession,
        token: JWTTokenStr,
    ) -> User:
        payload = decode_jwt(token=token)

        user = await cls.user_dao.get_user_by_email(
            session,
            payload.get("email"),
        )

        if user is None:
            raise HTTPException(
                status_code=401, detail="User not found, you need to login"
            )

        return user

    @classmethod
    async def get_user_by_email(
        cls,
        session: AsyncSession,
        email: str,
    ) -> User:
        return await cls.user_dao.get_user_by_email(session, email)

    @classmethod
    async def update_user_by_token(
        cls,
        session: AsyncSession,
        user_to_update: User,
        user_schema: UserUpdate,
    ) -> User:
        updated_user = await UserDAO.update(
            session=session,
            user_schema=user_schema,
            user_to_update=user_to_update,
            exclude_fields={"email", "password"},
        )

        input_email = user_schema.email
        old_email = updated_user.email

        if input_email and input_email != old_email:
            user_exists = await cls.user_dao.get_user_by_email(
                session=session, email=input_email
            )
            if user_exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this email already exists",
                )

        return updated_user

    @classmethod
    async def soft_delete_user_by_token(
        cls,
        session: AsyncSession,
        token: JWTTokenStr,
    ) -> None:
        user_to_delete = await cls.get_user_by_token(session, token)

        user_to_delete.is_active = False

        await session.commit()
        await session.flush(user_to_delete)
