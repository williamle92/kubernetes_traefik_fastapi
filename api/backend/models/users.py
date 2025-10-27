from enum import Enum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import ChoiceType

from backend.models.base import Base


class UserRole(Enum):
    USER: str = "user"
    SUPER_ADMIN: str = "super_admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    email: Mapped[str] = mapped_column(String(70), unique=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str] = mapped_column(String(20))
    phone_country_code: Mapped[str] = mapped_column(String(10), default="1", server_default="1")
    hashed_password: Mapped[str]
    permission: Mapped[UserRole] = mapped_column(
        ChoiceType(UserRole), default=UserRole.USER, server_default=UserRole.USER.value
    )
