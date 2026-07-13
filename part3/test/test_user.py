"""Test for User class."""

import unittest

from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.user import User


class TestUserClass(unittest.TestCase):
    def test_user_creation(self) -> None:
        print("\nRunning test_user_creation. : ", end="")
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password!",
        )
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.is_admin, False)  # Default value
