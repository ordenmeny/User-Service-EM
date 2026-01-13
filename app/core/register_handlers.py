from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from jwt.exceptions import ExpiredSignatureError
from sqlalchemy.exc import DatabaseError
import logging
from app.core.custom_exceptions import UserNotActiveException

logger = logging.getLogger(__name__)



def register_exception_handlers(app: FastAPI):
    @app.exception_handler(ExpiredSignatureError)
    async def expired_signature_error(
        request: Request,
        exc: ExpiredSignatureError,
    ):
        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": "Неверный токен или срок действия истек",
            },
        )

    @app.exception_handler(DatabaseError)
    async def handle_database_error(
        request: Request,
        exc: DatabaseError,
    ):
        logger.error("Database error", exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Ошибка базы данных",
            },
        )

    @app.exception_handler(UserNotActiveException)
    async def handle_user_not_active_error(
        request: Request,
        exc: UserNotActiveException,
    ):
        return ORJSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": "user not active",
            },
        )


