import jwt
from app.core.config import settings
import bcrypt
from datetime import datetime, UTC


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    exp=settings.auth_jwt.access_token_exp,
):
    to_encode = payload.copy()
    now = datetime.now(UTC)
    exp = now + exp

    to_encode.update({"exp": exp, "iat": now})

    return jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )


def decode_jwt(
    token: str,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    return jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm],
    )


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
