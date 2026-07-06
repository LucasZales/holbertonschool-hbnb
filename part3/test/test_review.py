"""Test for Review class."""

import unittest

from app.models.user import User
from app.models.place import Place
from app.models.review import Review


class TestReviewClass(unittest.TestCase):
    def test_review_creation(self) -> None:
        print("Running test_review_creation.")
        user = User(
            first_name="Ricardo",
            last_name="Lopez",
            email="Ricardo.Lopez@example.com",
            password="password!",
        )

        place = Place(
            title="Beach House",
            price=100,
            latitude=10,
            longitude=10,
            owner=user,
        )

        review = Review(text="Amazing Place", rating=3, user=user, place=place)
        place.add_review(review)

        self.assertEqual(review.text, "Amazing Place")
        self.assertEqual(review.rating, 3)
        self.assertEqual(review.user_id, user.id)
        self.assertEqual(review.place_id, place.id)
        self.assertEqual(len(place.reviews), 1)
