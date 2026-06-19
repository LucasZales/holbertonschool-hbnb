"""Test for user class."""

import unittest
from app.models.user import User


class test_user_class(unittest.TestCase):
    def test_user_creation(self):
        user = User(
            first_name="John", last_name="Doe", email="john.doe@example.com"
        )
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.is_admin, False)  # Default value
