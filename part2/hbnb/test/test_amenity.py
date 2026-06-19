"""Test for user class."""

import unittest
from app.models.amenity import Amenity


class test_amenity_class(unittest.TestCase):
    def test_amenity_creation(self):
        amenity = Amenity(name="Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")
