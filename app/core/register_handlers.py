from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from jwt.exceptions import PyJWTError
from sqlalchemy.exc import DatabaseError
import logging
from app.core.custom_exceptions import (
    UserNotActiveException,
    InvalidCredentialsError,
)
from fastapi.encoders import jsonable_encoder


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
                "detail": "Bad credentials",
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

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        try:
            type_er = exc.errors()[0].get('type')
            loc_er = ' '.join(exc.errors()[0].get('loc'))
        except:
            type_er = 'ValidationError'
            loc_er = 'Unknown'
        return ORJSONResponse(
            status_code=422,
            content={"detail": f'{type_er} {loc_er}', "body": exc.body},
        )
