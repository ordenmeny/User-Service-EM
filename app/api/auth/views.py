from fastapi import APIRouter
from app.db.dependencies import SessionDep
from .schemas import UserLoginSchema, UserCreate, UserRead
from .models import User
from app.core.utils import hash_password, encode_jwt, check_password
from sqlalchemy import select

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register")
async def register(
    user_schema: UserCreate,
    session: SessionDep,
):
    user = user_schema.model_dump(exclude={"password2"})
    password = user.pop("password")
    user["password"] = hash_password(password)
    user_db = User(**user)

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)

    payload = {
        "sub": user_db.id,
        "email": user_db.email,
    }

    access_token = encode_jwt(payload)

    return {
        "access_token": access_token,
        "user": UserRead.model_validate(user_db),
    }


@auth_router.post("/login")
async def login(
    user: UserLoginSchema,
    session: SessionDep,
):
    stmt = select(User).where(User.email == user.email)
    result = await session.execute(stmt)
    user_db = result.scalar_one_or_none()

    if user_db is None:
        return {"error": "user not found"}

    input_password = user.password
    hashed_password = str(user_db.password)

    if not check_password(input_password, hashed_password):
        return {"error": "password not correct"}

    payload = {
        "sub": user_db.id,
        "email": user_db.email,
    }

    access_token = encode_jwt(payload)

    return {
        "access_token": access_token,
    }
