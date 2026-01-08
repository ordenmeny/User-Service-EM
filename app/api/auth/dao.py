from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User
from .utils import hash_password


class UserDAO:
    user_model = User

    @classmethod
    async def get_user_by_email(
        cls,
        session: AsyncSession,
        email: str,
    ) -> User | None:
        stmt = select(cls.user_model).where(cls.user_model.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
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
