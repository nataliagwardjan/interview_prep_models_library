import unittest
from datetime import datetime, timezone
from uuid import uuid4
from models import (
    UserCreateSchema,
    UserSchema,
    UserLoginSchema,
    Role
)
from pydantic import ValidationError


class UserTestWithUnitest(unittest.TestCase):
    def test_user_create_schema_valid(self):
        user = UserCreateSchema(
            first_name="John",
            surname="Doe",
            email="john.doe@example.com",
            password="StrongP@ssword1",
            confirm_password="StrongP@ssword1",
        )
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.surname, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.password, "StrongP@ssword1")
        self.assertEqual(user.confirm_password, user.password)

    def test_user_create_schema_invalid_password(self):
        with self.assertRaises(ValidationError) as context:
            UserCreateSchema(
                first_name="John",
                surname="Doe",
                email="john.doe@example.com",
                password="weakpass",
                confirm_password="weakpass"
            )
        self.assertIn("Password must be at least 10 characters long.", str(context.exception))
        self.assertIn("Password must contain at least one uppercase letter.", str(context.exception))

    def test_user_create_schema_password_mismatch(self):
        with self.assertRaises(ValidationError) as context:
            UserCreateSchema(
                first_name="John",
                surname="Doe",
                email="john.doe@example.com",
                password="StrongP@ssword1",
                confirm_password="WrongConfirmP@ssword1",
            )
        self.assertIn("Passwords do not match", str(context.exception))

    def test_user_schema_valid(self):
        create_datetime = datetime.now(timezone.utc)
        user = UserSchema(
            id=uuid4(),
            first_name="Alice",
            surname="Smith",
            username_email="alice.smith@example.com",
            roles=[Role.REGULAR, Role.ADMIN],
            tests=[],
            create_datetime=create_datetime
        )
        self.assertEqual(user.first_name, "Alice")
        self.assertEqual(user.surname, "Smith")
        self.assertEqual(user.username_email, "alice.smith@example.com")
        self.assertEqual(user.create_datetime, create_datetime)
        self.assertIn(Role.REGULAR, user.roles)
        self.assertIn(Role.ADMIN, user.roles)

    def test_user_schema_invalid_email(self):
        with self.assertRaises(ValidationError):
            UserSchema(
                id=uuid4(),
                first_name="Alice",
                surname="Smith",
                username_email="invalid-email",
                roles=[Role.REGULAR],
                tests=[]
            )

    def test_user_schema_default_role(self):
        user = UserSchema(
            id=uuid4(),
            first_name="Bob",
            surname="Brown",
            username_email="bob.brown@example.com",
            tests=[]
        )
        self.assertEqual(user.roles, [Role.REGULAR])  # Default role

    def test_user_login_schema_valid(self):
        login_data = UserLoginSchema(
            username="testuser",
            password="StrongP@ssword1",
        )
        self.assertEqual(login_data.username, "testuser")
        self.assertEqual(login_data.password, "StrongP@ssword1")

    def test_user_login_schema_missing_fields(self):
        with self.assertRaises(ValidationError):
            UserLoginSchema(
                username="testuser"
            )

    def test_user_login_schema_empty_username(self):
        with self.assertRaises(ValidationError):
            UserLoginSchema(
                password="StrongP@ssword1"
            )

    def test_user_login_schema_blank_username(self):
        with self.assertRaises(ValidationError):
            UserLoginSchema(
                username="",
                password="StrongP@ssword1"
            )


if __name__ == "__main__":
    unittest.main()
