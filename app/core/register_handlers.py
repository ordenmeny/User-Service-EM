from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from jwt.exceptions import PyJWTError
from sqlalchemy.exc import DatabaseError
import logging
from app.core.custom_exceptions import (
    UserNotActiveException,
    InvalidCredentialsError,
)

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(PyJWTError)
    async def expired_signature_error(
        request: Request,
        exc: PyJWTError,
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
            status_code=exc.code,
            content={
                "detail": exc.message,
            },
        )

    @app.exception_handler(InvalidCredentialsError)
    async def handle_exception(
        request: Request,
        exc: InvalidCredentialsError,
    ):
        return ORJSONResponse(
            status_code=exc.code,
            content={
                "detail": exc.message,
            },
        )
