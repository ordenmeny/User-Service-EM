from .base_dao import BaseUserDAO
from .models import User
from .schemas import UserUpdate


class UserDAO(BaseUserDAO[User, UserUpdate]):
    user_model = User
