from fastapi import FastAPI
from jwt.exceptions import ExpiredSignatureError
from app.api.auth.exception_handlers import expired_signature_error


def register_exception_handler(app: FastAPI):
    app.add_exception_handler(
        ExpiredSignatureError,  # raising Exception
        expired_signature_error,  # handler
    )
