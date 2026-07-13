"""Test for Amenity class."""

import unittest

from app.models.amenity import Amenity


class TestAmenityClass(unittest.TestCase):
    def test_amenity_creation(self) -> None:
        print("\nRunning test_amenitty_class. : ", end="")
        amenity = Amenity(name="Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")
