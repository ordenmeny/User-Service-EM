from fastapi import HTTPException, status
from .schemas import UserCreate, UserRead, JWTToken
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import encode_jwt, check_password, decode_jwt
from .dao import UserDAO
from .models import User


class AuthService:
    @classmethod
    async def create_token(cls, user_db: User) -> JWTToken:
        payload = {
            "sub": str(user_db.id),
            "email": user_db.email,
        }

        return JWTToken(
            token=encode_jwt(payload),
            token_type="bearer",
        )


class UserService:
    user_dao = UserDAO

    @classmethod
    async def login(cls, session: AsyncSession, user: UserRead) -> JWTToken:

        user_db = await cls.user_dao.get_user_by_email(session, user.email)

        if user_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        input_password = user.password
        hashed_password = str(user_db.password)

        if not check_password(input_password, hashed_password):
            return {"error": "password not correct"}

        access_token = await AuthService.create_token(user_db)

        return access_token

    @classmethod
    async def register_new_user(
        cls,
        session: AsyncSession,
        user_schema: UserCreate,
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

        access_token = await AuthService.create_token(user_db)

        return {
            "access_token": access_token,
            "user": UserRead.model_validate(user_db),
        }

    @classmethod
    async def get_user_by_token(
        cls,
        session: AsyncSession,
        token: JWTToken,
    ):
        payload = decode_jwt(token=token)

        return await cls.user_dao.get_user_by_email(
            session,
            payload.get("email"),
        )
