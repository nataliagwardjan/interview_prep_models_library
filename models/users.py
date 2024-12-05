from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationInfo
from typing import Optional, List
from uuid import UUID
from enum import Enum
from datetime import datetime, timezone
import re


class Role(str, Enum):
    REGULAR = 'REGULAR'
    MANAGER = 'MANAGER'
    ADMIN = 'ADMIN'
    DB_MANAGEMENT_SERVICE = 'DB_MANAGEMENT_SERVICE'
    AUTH_SERVICE = 'AUTH_SERVICE'
    TESTS_SERVICE = 'TESTS_SERVICE'


class UserCreateSchema(BaseModel):
    first_name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """
        Password validation:
        * at least 10 characters,
        * at least one lowercase letter,
        * at least one uppercase letter,
        * at least one digit,
        * at least one special character.
        """
        message = ""
        if len(value) < 10:
            message += "Password must be at least 10 characters long.\n"
        if not re.search(r"[a-z]", value):
            message += "Password must contain at least one lowercase letter.\n"
        if not re.search(r"[A-Z]", value):
            message += "Password must contain at least one uppercase letter.\n"
        if not re.search(r"\d", value):
            message += "Password must contain at least one digit.\n"
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            message += "Password must contain at least one special character.\n"

        if message != "":
            raise ValueError(message)
        return value

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, confirm_password: str, info: ValidationInfo) -> str:
        """
        Confirm password validator: Must to be identical as `password`.
        """
        if "password" in info.data and confirm_password != info.data["password"]:
            raise ValueError("Passwords do not match")
        return confirm_password


class UserSchema(BaseModel):
    id: UUID
    first_name: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=50)
    username_email: EmailStr
    roles: List[Role] = Field(..., default_factory=lambda: [Role.REGULAR])
    tests: Optional[List] = Field(default_factory=list)
    create_datetime: datetime = Field(default=datetime.now(timezone.utc).isoformat())


class UserLoginSchema(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def username_not_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("Username cannot be empty")
        return value

    @field_validator("password")
    @classmethod
    def password_not_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("Password cannot be empty")
        return value
