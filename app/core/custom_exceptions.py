from fastapi import status


class BaseError(Exception):
    """Базовая ошибка приложения."""

    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code
        super().__init__(message)


class UserNotActiveException(BaseError):
    def __init__(
        self,
        message: str = "User not active",
        code: int = status.HTTP_403_FORBIDDEN,
    ):
        super().__init__(message=message, code=code)


class InvalidCredentialsError(BaseError):
    def __init__(
        self,
        message: str = "Invalid credentials",
        code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(message=message, code=code)



class CustomDatabaseError(BaseError):
    def __init__(
        self,
        message: str = "Invalid credentials",
        code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(message=message, code=code)
