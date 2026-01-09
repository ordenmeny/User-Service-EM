from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User
from .utils import hash_password
from pydantic import BaseModel


class UserDAO:
    user_model = User

    @classmethod
    async def get_user_by_email(
        cls,
        session: AsyncSession,
        email: str,
    ):
        stmt = select(cls.user_model).where(cls.user_model.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user.is_active:
            raise HTTPException(
                status_code=403,
                detail="User is not active",
            )

        return user

    @classmethod
    async def add_to_db(
        cls,
        session: AsyncSession,
        user: dict,
    ) -> User:
        user = user.copy()

        password = user.pop("password")
        user["password"] = hash_password(password)

        user_db = cls.user_model(**user)

        session.add(user_db)
        await session.commit()
        await session.refresh(user_db)

        return user_db

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        user_schema,
        user_to_update,
        exclude_fields: set,
    ):
        for field, value in user_schema.model_dump(exclude_none=True).items():
            if field in exclude_fields:
                continue

            if field is not None:
                setattr(user_to_update, field, value)

        await session.commit()
        await session.refresh(user_to_update)

        return user_to_update
