from fastapi import HTTPException, status
from jwt.exceptions import ExpiredSignatureError
from fastapi import Request


async def expired_signature_error(
    request: Request,
    exc: ExpiredSignatureError,
):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный токен или срок действия истек",
    )
