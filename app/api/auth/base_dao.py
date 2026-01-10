from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .utils import hash_password
from app.core.custom_exceptions import (
    UserNotActiveException,
)
from typing import Generic, Type
from app.core.type_vars import UserType, UpdateSchemaType


class BaseUserDAO(Generic[UserType, UpdateSchemaType]):
    user_model: Type[UserType]

    @classmethod
    async def get_user_by_email(
        cls,
        session: AsyncSession,
        email: str,
    ) -> UserType | None:
        stmt = select(cls.user_model).where(cls.user_model.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user and not user.is_active:
            raise UserNotActiveException()

        return user

    @classmethod
    async def add_to_db(
        cls,
        session: AsyncSession,
        user: dict,
    ) -> UserType:
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
        user_schema: UpdateSchemaType,
        user_to_update: UserType,
        exclude_fields: set[str],
    ) -> UserType:

        for field, value in user_schema.model_dump(exclude_none=True).items():
            if field in exclude_fields:
                continue

            if value is not None:
                setattr(user_to_update, field, value)

        await session.commit()
        await session.refresh(user_to_update)

        return user_to_update
