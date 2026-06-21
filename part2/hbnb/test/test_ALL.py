"""One test to rule them all."""

from typing import Reversible
import unittest
import requests
import json


class TestALL(unittest.TestCase):
    """Test for Everything."""

    def test_everything(self) -> None:
        """"""
        url = "http://localhost:5000/api/v1"
        headers = {"Content-Type": "application/json"}
        user_one_init = {
            "first_name": "John",
            "last_name": "doe",
            "email": "john.doe@example.com",
        }
        user_two_init = {
            "first_name": "Jane",
            "last_name": "doe",
            "email": "jake.doe@example.com",
        }
        user_two_update = {
            "first_name": "Jane",
            "last_name": "doe",
            "email": "jane.doe@example.com",
        }

        user_one_full = requests.post(
            f"{url}/users/",
            data=json.dumps(user_one_init),
            headers=headers,
            timeout=5,
        ).json()

        user_two_full = requests.post(
            f"{url}/users/",
            data=json.dumps(user_two_init),
            headers=headers,
            timeout=5,
        ).json()

        user_one_id = user_one_full["id"]
        user_two_id = user_two_full["id"]

        user_two_updated = requests.put(
            f"{url}/users/{user_two_id}",
            data=json.dumps(user_two_update),
            headers=headers,
            timeout=5,
        ).json()

        user_one_details = requests.get(
            f"{url}/users/{user_one_id}",
            headers=headers,
            timeout=5,
        ).json()

        userlist = requests.get(
            f"{url}/users/",
            headers=headers,
            timeout=5,
        ).json()

        place_one_init = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user_one_id,
        }

        place_two_init = {
            "title": "Luxury Penhouse",
            "description": "An expensive place",
            "price": 10000.0,
            "latitude": 59.7549,
            "longitude": -141.41134,
            "owner_id": user_two_id,
        }

        place_two_update = {
            "title": "Luxury-er Penhouse",
            "description": "Luxury condo",
            "price": 10500.0,
            "latitude": 59.7549,
            "longitude": -141.41134,
            "owner_id": user_two_id,
        }

        place_one_full = requests.post(
            f"{url}/places/",
            data=json.dumps(place_one_init),
            headers=headers,
            timeout=5,
        ).json()

        place_two_full = requests.post(
            f"{url}/places/",
            data=json.dumps(place_two_init),
            headers=headers,
            timeout=5,
        ).json()

        place_one_id = place_one_full["id"]
        place_two_id = place_two_full["id"]

        place_two_updated = requests.put(
            f"{url}/places/{place_two_id}",
            data=json.dumps(place_two_update),
            headers=headers,
            timeout=5,
        ).json()

        place_one_details = requests.get(
            f"{url}/places/{place_one_id}",
            headers=headers,
            timeout=5,
        ).json()

        placelist = requests.get(
            f"{url}/places/",
            headers=headers,
            timeout=5,
        ).json()

        amenity_one_init = {"name": "Wi-Fi"}
        amenity_two_init = {"name": "Air Conditioning"}
        amenity_two_update = {"name": "Heating"}

        amenity_one_full = requests.post(
            f"{url}/amenities/",
            data=amenity_one_init,
            headers=headers,
            timeout=5,
        ).json()

        amenity_two_full = requests.post(
            f"{url}/amenities/",
            data=amenity_two_init,
            headers=headers,
            timeout=5,
        ).json()

        amenity_two_updated = requests.put(
            f"{url}/amenities/",
            data=amenity_two_update,
            headers=headers,
            timeout=5,
        ).json()

        amenity_one_details = requests.get(
            f"{url}/amenities/{user_one_full['id']}",
            headers=headers,
            timeout=5,
        ).json()

        amenitylist = requests.get(
            f"{url}/amenities/",
            headers=headers,
            timeout=5,
        ).json()

        review_one_init = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user_one_id,
            "place_id": place_two_id,
        }

        review_two_init = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user_two_id,
            "place_id": place_one_id,
        }

        review_two_update = {
            "text": "Amazing stay!",
            "rating": 4,
        }

        review_one_full = requests.post(
            f"{url}/reviews/",
            data=json.dumps(review_one_init),
            headers=headers,
            timeout=5,
        ).json()

        review_two_full = requests.post(
            f"{url}/reviews/",
            data=json.dumps(review_two_init),
            headers=headers,
            timeout=5,
        ).json()

        review_one_id = review_one_full["id"]
        review_two_id = review_two_full["id"]

        review_two_updated = requests.put(
            f"{url}/reviews/{review_two_id}",
            data=json.dumps(review_two_update),
            headers=headers,
            timeout=5,
        ).json()

        review_one_details = requests.get(
            f"{url}/reviews/{review_one_id}",
            headers=headers,
            timeout=5,
        ).json()

        reviewlist_pre = requests.get(
            f"{url}/reviews/",
            headers=headers,
            timeout=5,
        ).json()

        review_two_del = requests.delete(
            f"{url}/reviews/{review_two_id}",
            timeout=5,
        )

        reviewlist_post = requests.get(
            f"{url}/reviews/",
            headers=headers,
            timeout=5,
        ).json()

        place_one_reviews = requests.get(
            f"{url}/places/{place_one_id}/reviews",
            headers=headers,
            timeout=5,
        )
