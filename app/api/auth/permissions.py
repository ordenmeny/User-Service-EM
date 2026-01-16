from app.core.custom_exceptions import InvalidCredentialsError
from fastapi.exceptions import HTTPException
from typing import Callable
from typing import Awaitable
from fastapi import Depends, status
from .models import User
from .dependencies import CurrentUserDep


def permission(msg: str):
    def decorator(func: Callable[[User], Awaitable[bool]]):
        async def wrapper(current_user: CurrentUserDep):
            if current_user is None:
                raise InvalidCredentialsError()

            is_req = await func(current_user)

            if not is_req:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=msg,
                )

        return wrapper

    return decorator


@permission("For admin only")
async def perm_admin_required(
    current_user: User,
) -> bool:
    return current_user.is_admin


admin_required = Depends(perm_admin_required)
