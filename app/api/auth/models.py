from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, false, true


class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    patronymic: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(
        String(255),
        index=True,
        unique=True,
    )
    password: Mapped[str]
    superuser: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        server_default=false(),
    )
    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
        server_default=true(),
    )
