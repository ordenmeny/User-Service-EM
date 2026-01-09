import jwt
from app.core.config import settings
import bcrypt
from datetime import datetime, UTC
from .custom_types import JWTTokenStr

from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from jwt.exceptions import ExpiredSignatureError


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    exp=settings.auth_jwt.access_token_lifetime,
) -> JWTTokenStr:
    to_encode = payload.copy()
    now = datetime.now(UTC)
    exp = now + exp

    to_encode.update({"exp": exp, "iat": now})

    token = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )
    return token


def decode_jwt(
    token: JWTTokenStr,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:

    decode = jwt.decode(
        jwt=token.encode("utf-8"),
        key=public_key,
        algorithms=[algorithm],
    )
    return decode


def hash_password(
    password: str,
) -> str:
    hashed_bytes: bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")


def check_password(
    password: str,
    hashed: str,
) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed.encode("utf-8"),
    )
