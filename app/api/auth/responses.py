from .schemas import UserReadWithToken, DetailResponse, JWTToken
from app.core.response_templates import detail_with_msg

register_response = {
    200: {
        "description": "Пользователь успешно зарегистрирован",
        "model": UserReadWithToken,
    },
    409: {
        "description": "User already exists",
        **detail_with_msg("User already exists"),
        "model": DetailResponse,
    },
}

login_response = {
    200: {
        "description": "Пользователь успешно авторизован",
    },
    401: {
        "description": "Неверный email или пароль",
        **detail_with_msg("Invalid credentials"),
        "model": DetailResponse,
    },
}

get_current_user_response = {
    200: {
        "description": "Пользователь успешно получен",
    },
    401: {
        "description": "Токен истек или неверный",
        **detail_with_msg("Bad credentials"),
        "model": DetailResponse,
    }
}

update_current_user_response = {
    200: {
        "description": "Пользователь успешно обновлен",
    },
    401: {
        "description": "Токен истек или неверный",
        **detail_with_msg("Bad credentials"),
        "model": DetailResponse,
    },
    409: {
        "description": "Пользователь с таким email уже существует",
        **detail_with_msg("User with this email already exists"),
        "model": DetailResponse,
    }
}

delete_current_user_response = {
    200: {
        "description": "Пользователь успешно удален",
    },
    401: {
        "description": "Токен истек или неверный",
        **detail_with_msg("Bad credentials"),
        "model": DetailResponse,
    },
}

logout_response = {
    200: {
        "description": "Пользователь успешно вышел из системы (refresh токен удален)",
        **detail_with_msg("logout"),
    },
}

refresh_response = {
    200: {
        "description": "Токен успешно обновлен",
    },
    401: {
        "description": "Токен истек или неверный",
        **detail_with_msg("Bad credentials"),
        "model": DetailResponse,
    },
}

example_admin_resource_response = {
    200: {
        "description": "Пример ресурса для администратора"
    },
    403: {
        "description": "Доступ разрешен только для администратора",
        **detail_with_msg("Bad credentials"),
        "model": DetailResponse,
    }
}