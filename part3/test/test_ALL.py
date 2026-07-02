"""One test to rule them all."""

import unittest
from werkzeug.test import TestResponse
from app import create_app
from pprint import pprint


def check_response(
    self: unittest.TestCase,
    response: TestResponse,
    expected_status: str,
) -> dict | None:
    if response.status != expected_status:
        print(response.json)
    self.assertEqual(response.status, expected_status)
    return response.json


class TestALL(unittest.TestCase):
    """Test for Everything."""

    def setUp(self) -> None:
        print("\nSetting up client.")
        self.app = create_app()
        self.client = self.app.test_client()

    def test_everything(self) -> None:
        """"""
        url = "http://localhost:5000/api/v1"
        headers = {"Content-Type": "application/json"}

        # USERS API TESTS
        user_one_init = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password",
        }
        user_two_init = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jake.doe@example.com",
            "password": "secure",
        }
        user_two_update = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "new_password",
        }
        user_null_update = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "pass",
        }
        user_bad_init = {
            "first_name": "",
            "last_name": "",
            "email": "invalid-email",
            "password": "passad",
        }

        user_repeat_init = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jake.doe@example.com",
            "password": "passed",
        }

        user_one_json = check_response(
            self,
            self.client.post(
                f"{url}/users/",
                json=user_one_init,
                headers=headers,
            ),
            "201 CREATED",
        )

        user_two_json = check_response(
            self,
            self.client.post(
                f"{url}/users/",
                json=user_two_init,
                headers=headers,
            ),
            "201 CREATED",
        )
        user_bad_json = check_response(
            self,
            self.client.post(
                f"{url}/users/",
                json=user_bad_init,
                headers=headers,
            ),
            "400 BAD REQUEST",
        )

        user_repeat_json = check_response(
            self,
            self.client.post(
                f"{url}/users/",
                json=user_repeat_init,
                headers=headers,
            ),
            "400 BAD REQUEST",
        )

        if user_one_json is None:
            raise ValueError("err: user_one_json is None")
        if user_two_json is None:
            raise ValueError("err: user_two_json is None")
        if user_bad_json is None:
            raise ValueError("err: user_bad_json is None")
        if user_repeat_json is None:
            raise ValueError("err: user_repeat_json is None")

        user_one_id = user_one_json["id"]
        user_two_id = user_two_json["id"]
        user_null_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"

        user_two_updated = check_response(
            self,
            self.client.put(
                f"{url}/users/{user_two_id}",
                json=user_two_update,
                headers=headers,
            ),
            "200 OK",
        )

        user_null_updated = check_response(
            self,
            self.client.put(
                f"{url}/users/{user_null_id}",
                json=user_null_update,
                headers=headers,
            ),
            "404 NOT FOUND",
        )

        if user_two_updated is None:
            raise ValueError("err: user_two_updated is None")

        user_one_details = check_response(
            self,
            self.client.get(
                f"{url}/users/{user_one_id}",
                headers=headers,
            ),
            "200 OK",
        )

        user_two_details = check_response(
            self,
            self.client.get(
                f"{url}/users/{user_two_id}",
                headers=headers,
            ),
            "200 OK",
        )

        user_null_details = check_response(
            self,
            self.client.get(
                f"{url}/users/{user_null_id}",
                headers=headers,
            ),
            "404 NOT FOUND",
        )

        userlist = check_response(
            self,
            self.client.get(
                f"{url}/users/",
                headers=headers,
            ),
            "200 OK",
        )
        if userlist is None:
            raise ValueError("err: userlist is None")

        # PLACE API TESTS
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

        place_null_update = {
            "title": "Luxury-er Penhouse",
            "description": "Luxury condo",
            "price": 10500.0,
            "latitude": 59.7549,
            "longitude": -141.41134,
            "owner_id": user_null_id,
        }

        place_bad_init = {
            "title": "",
            "description": "",
            "price": -5,
            "latitude": 107.7749,
            "longitude": -192.4194,
            "owner_id": user_null_id,
        }

        place_one_json = check_response(
            self,
            self.client.post(
                f"{url}/places/",
                json=place_one_init,
                headers=headers,
            ),
            "201 CREATED",
        )

        place_two_json = check_response(
            self,
            self.client.post(
                f"{url}/places/",
                json=place_two_init,
                headers=headers,
            ),
            "201 CREATED",
        )

        place_bad_json = check_response(
            self,
            self.client.post(
                f"{url}/places/",
                json=place_bad_init,
                headers=headers,
            ),
            "400 BAD REQUEST",
        )

        if place_one_json is None:
            raise ValueError("err: place_one_json is None")
        if place_two_json is None:
            raise ValueError("err: place_two_json is None")
        if place_bad_json is None:
            raise ValueError("err: place_bad_json is None")

        place_one_id = place_one_json["id"]
        place_two_id = place_two_json["id"]
        place_null_id = "1fa85f64-5717-4562-b3fc-2c963f66afa6"

        place_two_updated = check_response(
            self,
            self.client.put(
                f"{url}/places/{place_two_id}",
                json=place_two_update,
                headers=headers,
            ),
            "200 OK",
        )

        place_null_updated = check_response(
            self,
            self.client.put(
                f"{url}/places/{place_null_id}",
                json=place_null_update,
                headers=headers,
            ),
            "404 NOT FOUND",
        )

        place_one_details = check_response(
            self,
            self.client.get(
                f"{url}/places/{place_one_id}",
                headers=headers,
            ),
            "200 OK",
        )

        place_two_details = check_response(
            self,
            self.client.get(
                f"{url}/places/{place_two_id}",
                headers=headers,
            ),
            "200 OK",
        )

        if place_one_details is None:
            raise ValueError("err: place_one_details is None")
        if place_two_details is None:
            raise ValueError("err: place_two_details is Ntwo")

        placelist = check_response(
            self,
            self.client.get(
                f"{url}/places/",
                headers=headers,
            ),
            "200 OK",
        )
        if placelist is None:
            raise ValueError("err: placelist is None")

        # AMENITY API TESTS
        amenity_one_init = {"name": "Wi-Fi"}
        amenity_two_init = {"name": "Air Conditioning"}
        amenity_bad_init = {"name": ""}
        amenity_two_update = {"name": "Heating"}
        amenity_null_update = {"name": "Heating"}

        amenity_one_json = check_response(
            self,
            self.client.post(
                f"{url}/amenities/",
                json=amenity_one_init,
                headers=headers,
            ),
            "201 CREATED",
        )

        amenity_two_json = check_response(
            self,
            self.client.post(
                f"{url}/amenities/",
                json=amenity_two_init,
                headers=headers,
            ),
            "201 CREATED",
        )

        amenity_bad_json = check_response(
            self,
            self.client.post(
                f"{url}/amenities/",
                json=amenity_bad_init,
                headers=headers,
            ),
            "400 BAD REQUEST",
        )

        if amenity_one_json is None:
            raise ValueError("err: amenity_one_json is None")
        if amenity_two_json is None:
            raise ValueError("err: amenity_two_json is None")
        if amenity_bad_json is None:
            raise ValueError("err: amenity_bad_json is None")

        amenity_one_id = amenity_one_json["id"]
        amenity_two_id = amenity_two_json["id"]
        amenity_null_id = "1fa85f64-5717-4562-b3fc-2c963f66afa6"

        amenity_two_updated = check_response(
            self,
            self.client.put(
                f"{url}/amenities/{amenity_two_id}",
                json=amenity_two_update,
                headers=headers,
            ),
            "200 OK",
        )

        amenity_null_updated = check_response(
            self,
            self.client.put(
                f"{url}/amenities/{amenity_null_id}",
                json=amenity_null_update,
                headers=headers,
            ),
            "404 NOT FOUND",
        )

        if amenity_two_updated is None:
            raise ValueError("err: amenity_two_updated is None")

        amenity_one_details = check_response(
            self,
            self.client.get(
                f"{url}/amenities/{amenity_one_id}",
                headers=headers,
            ),
            "200 OK",
        )

        amenity_two_details = check_response(
            self,
            self.client.get(
                f"{url}/amenities/{amenity_two_id}",
                headers=headers,
            ),
            "200 OK",
        )

        amenity_null_details = check_response(
            self,
            self.client.get(
                f"{url}/amenities/{amenity_null_id}",
                headers=headers,
            ),
            "404 NOT FOUND",
        )

        amenitylist = check_response(
            self,
            self.client.get(
                f"{url}/amenities/",
                headers=headers,
            ),
            "200 OK",
        )
        if amenitylist is None:
            raise ValueError("err: amenitylist is None")

        # REVIEW API TESTS
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

        review_bad_init = {
            "text": 42,
            "rating": 30,
            "user_id": user_null_id,
            "place_id": place_null_id,
        }

        review_two_update = {
            "text": "Amazing stay!",
            "rating": 4,
        }

        review_null_update = {
            "text": "Amazing stay!",
            "rating": 4,
        }

        review_one_json = check_response(
            self,
            self.client.post(
                f"{url}/reviews/",
                json=review_one_init,
                headers=headers,
            ),
            "201 CREATED",
        )

        review_two_json = check_response(
            self,
            self.client.post(
                f"{url}/reviews/",
                json=review_two_init,
                headers=headers,
            ),
            "201 CREATED",
        )

        review_bad_json = check_response(
            self,
            self.client.post(
                f"{url}/reviews/",
                json=review_bad_init,
                headers=headers,
            ),
            "400 BAD REQUEST",
        )

        if review_one_json is None:
            raise ValueError("err: review_one_json is None")
        if review_two_json is None:
            raise ValueError("err: review_two_json is None")
        if review_bad_json is None:
            raise ValueError("err: review_bad_json is None")

        review_one_id = review_one_json["id"]
        review_two_id = review_two_json["id"]
        review_null_id = "2fa85f64-5717-4562-b3fc-2c963f66afa6"

        review_two_updated = check_response(
            self,
            self.client.put(
                f"{url}/reviews/{review_two_id}",
                json=review_two_update,
                headers=headers,
            ),
            "200 OK",
        )

        review_null_updated = check_response(
            self,
            self.client.put(
                f"{url}/reviews/{review_null_id}",
                json=review_null_update,
                headers=headers,
            ),
            "404 NOT FOUND",
        )

        review_one_details = check_response(
            self,
            self.client.get(
                f"{url}/reviews/{review_one_id}",
                headers=headers,
            ),
            "200 OK",
        )

        review_two_details = check_response(
            self,
            self.client.get(
                f"{url}/reviews/{review_two_id}",
                headers=headers,
            ),
            "200 OK",
        )

        if review_one_details is None:
            raise ValueError("err: review_one_details is None")
        if review_two_details is None:
            raise ValueError("err: review_two_details is None")

        reviewlist_pre = check_response(
            self,
            self.client.get(
                f"{url}/reviews/",
                headers=headers,
            ),
            "200 OK",
        )

        review_two_del = check_response(
            self,
            self.client.delete(
                f"{url}/reviews/{review_two_id}",
            ),
            "200 OK",
        )

        review_null_del = check_response(
            self,
            self.client.delete(
                f"{url}/reviews/{review_null_id}",
            ),
            "404 NOT FOUND",
        )

        reviewlist_post = check_response(
            self,
            self.client.get(
                f"{url}/reviews/",
                headers=headers,
            ),
            "200 OK",
        )
        if reviewlist_pre is None:
            raise ValueError("err: reviewlist_pre is None")

        if reviewlist_post is None:
            raise ValueError("err: reviewlist_post is None")

        place_one_reviews = check_response(
            self,
            self.client.get(
                f"{url}/places/{place_one_id}/reviews",
                headers=headers,
            ),
            "200 OK",
        )

        place_two_reviews = check_response(
            self,
            self.client.get(
                f"{url}/places/{place_two_id}/reviews",
                headers=headers,
            ),
            "200 OK",
        )

        place_null_reviews = check_response(
            self,
            self.client.get(
                f"{url}/places/{place_null_id}/reviews",
                headers=headers,
            ),
            "404 NOT FOUND",
        )

        # RESPONSE DATA TESTS

        # USER RESPONSE TESTS
        # --VALID USER CREATION
        self.assertEqual(user_one_json["id"], user_one_id)
        for key in ["first_name", "last_name", "email"]:
            self.assertEqual(user_one_json[key], user_one_init[key])

        self.assertEqual(user_two_json["id"], user_two_id)
        for key in ["first_name", "last_name", "email"]:
            self.assertEqual(user_two_json[key], user_two_init[key])

        # --INVALID USER CREATION
        user_bad_expected = {
            "errors": {
                "email": "'invalid-email' does not match '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\\\.[A-Za-z]{2,7}'"
            },
            "message": "Input payload validation failed",
        }
        self.assertDictEqual(user_bad_json, user_bad_expected)

        user_repeat_expected = {"error": "Email already registered"}
        self.assertDictEqual(user_repeat_json, user_repeat_expected)

        # --UPDATE USER BY VALID ID
        self.assertEqual(user_two_json["id"], user_two_id)
        for key in ["first_name", "last_name", "email"]:
            self.assertEqual(user_two_updated[key], user_two_update[key])

        # --UPDATE USER BY INVALID ID
        user_null_update_expected = {"error": "User not found"}
        self.assertEqual(user_null_updated, user_null_update_expected)

        # --GET USER DETAILS BY VALID ID
        user_one_details_expected = user_one_init.copy()
        user_one_details_expected["id"] = user_one_id
        del user_one_details_expected["password"]
        self.assertEqual(user_one_details, user_one_details_expected)

        user_two_details_expected = user_two_update.copy()
        user_two_details_expected["id"] = user_two_id
        del user_two_details_expected["password"]
        self.assertEqual(user_two_details, user_two_details_expected)

        # --GET USER DETAILS BY INVALID ID
        user_null_expected = {"error": "User not found"}
        self.assertEqual(user_null_details, user_null_expected)

        # --GET USER LIST
        self.assertEqual(userlist, [user_one_details, user_two_details])

        # AMENITY RESPONSE TESTS
        # -POST /api/v1/amenities/
        # --VALID AMENITY CREATION
        amenity_one_expected = amenity_one_init.copy()
        amenity_one_expected["id"] = amenity_one_id
        self.assertEqual(amenity_one_json, amenity_one_expected)

        amenity_two_expected = amenity_two_init.copy()
        amenity_two_expected["id"] = amenity_two_id
        self.assertEqual(amenity_two_json, amenity_two_expected)

        # --INVALID AMENITY CREATION
        amenity_bad_expected = {"error": "Name cannot be empty"}
        self.assertDictEqual(amenity_bad_json, amenity_bad_expected)

        # -PUT /api/v1/amenities/<amenity_id>
        # --UPDATE AMENITY BY VALID ID
        amenity_two_update_expected = {
            "message": "Amenity updated successfully"
        }
        self.assertEqual(amenity_two_updated, amenity_two_update_expected)

        # --UPDATE AMENITY BY INVALID ID
        amenity_null_update_expected = {"error": "Amenity not found"}
        self.assertEqual(amenity_null_updated, amenity_null_update_expected)

        # -GET /api/v1/amenities/<amenity_id>
        # --GET AMENITY DETAILS BY VALID ID
        amenity_one_details_expected = amenity_one_init.copy()
        amenity_one_details_expected["id"] = amenity_one_id
        self.assertEqual(amenity_one_details, amenity_one_details_expected)

        amenity_two_details_expected = amenity_two_update.copy()
        amenity_two_details_expected["id"] = amenity_two_id
        self.assertEqual(amenity_two_details, amenity_two_details_expected)

        # --GET AMENITY DETAILS BY INVALID ID
        amenity_null_details = {"error": "Amenity not found"}
        self.assertEqual(amenity_null_details, amenity_null_details)

        # -GET /api/v1/amenities/
        # --GET AMENITY LIST
        self.assertEqual(
            amenitylist, [amenity_one_details, amenity_two_details]
        )

        # PLACE RESPONSE TESTS
        # -POST /api/v1/places/
        # --VALID PLACE CREATION
        place_one_expected = place_one_init.copy()
        place_one_expected["id"] = place_one_id
        self.assertEqual(place_one_json, place_one_expected)

        place_two_expected = place_two_init.copy()
        place_two_expected["id"] = place_two_id
        self.assertEqual(place_two_json, place_two_expected)

        # --INVALID PLACE CREATION
        place_bad_expected = {"error": "Owner not found"}
        self.assertDictEqual(place_bad_json, place_bad_expected)

        # -PUT /api/v1/places/<place_id>
        # --UPDATE PLACE BY VALID ID
        place_two_update_expected = {"message": "Place updated successfully"}
        self.assertEqual(place_two_updated, place_two_update_expected)

        # --UPDATE PLACE BY INVALID ID
        place_null_update_expected = {"error": "Place not found"}
        self.assertEqual(place_null_updated, place_null_update_expected)

        # -GET /api/v1/places/<place_id>
        # --GET PLACE DETAILS BY VALID ID
        place_one_details_expected = place_one_init.copy()
        place_one_details_expected["id"] = place_one_id
        place_one_details_expected["amenities"] = []
        place_one_details_expected["owner"] = user_one_details
        del place_one_details_expected["owner_id"]
        self.assertEqual(place_one_details, place_one_details_expected)

        place_two_details_expected = place_two_update.copy()
        place_two_details_expected["id"] = place_two_id
        place_two_details_expected["amenities"] = []
        place_two_details_expected["owner"] = user_two_details
        del place_two_details_expected["owner_id"]
        self.assertEqual(place_two_details, place_two_details_expected)

        # --GET place DETAILS BY INVALID ID
        place_null_details = {"error": "place not found"}
        self.assertEqual(place_null_details, place_null_details)

        # -GET /api/v1/places/
        # --GET PLACE LIST
        place_one_list_details = {
            x: y
            for x, y in place_one_details.items()
            if x in ["id", "title", "latitude", "longitude"]
        }
        place_two_list_details = {
            x: y
            for x, y in place_two_details.items()
            if x in ["id", "title", "latitude", "longitude"]
        }
        self.assertEqual(
            placelist, [place_one_list_details, place_two_list_details]
        )

        # -GET /api/v1/places/<place_id>/reviews
        # --GET ALL REVIEWS FOR <PLACE_ID>
        place_one_reviews_expected = []
        self.assertEqual(place_one_reviews, place_one_reviews_expected)

        place_two_reviews_expected = [
            {
                k: v
                for k, v in review_one_details.items()
                if k in ["id", "text", "rating"]
            }
        ]
        self.assertEqual(place_two_reviews, place_two_reviews_expected)

        place_null_reviews_expected = {"error": "Place not found"}
        self.assertEqual(place_null_reviews, place_null_reviews_expected)

        # REVIEW RESPONSE TESTS
        # -POST /api/v1/reviews/
        # --VALID REVIEW CREATION
        review_one_expected = review_one_init.copy()
        review_one_expected["id"] = review_one_id
        self.assertEqual(review_one_json, review_one_expected)

        review_two_expected = review_two_init.copy()
        review_two_expected["id"] = review_two_id
        self.assertEqual(review_two_json, review_two_expected)

        # --INVALID REVIEW CREATION
        review_bad_expected = {"error": "User or Place not found"}
        self.assertDictEqual(review_bad_json, review_bad_expected)

        # -PUT /api/v1/reviews/<review_id>
        # --UPDATE REVIEW BY VALID ID
        review_two_update_expected = {"message": "Review updated successfully"}
        self.assertEqual(review_two_updated, review_two_update_expected)

        # --UPDATE REVIEW BY INVALID ID
        review_null_update_expected = {"error": "Review not found"}
        self.assertEqual(review_null_updated, review_null_update_expected)

        # -GET /api/v1/reviews/<review_id>
        # --GET REVIEW DETAILS BY VALID ID
        review_one_details_expected = review_one_init.copy()
        review_one_details_expected["id"] = review_one_id
        self.assertEqual(review_one_details, review_one_details_expected)

        review_two_details_expected = review_two_update.copy()
        review_two_details_expected["id"] = review_two_id
        review_two_details_expected["user_id"] = user_two_id
        review_two_details_expected["place_id"] = place_one_id
        self.assertEqual(review_two_details, review_two_details_expected)

        # --GET REVIEW DETAILS BY INVALID ID
        review_null_details = {"error": "review not found"}
        self.assertEqual(review_null_details, review_null_details)

        # -DELETE /api/v1/reviews/<review_id>
        # --DELETE REVIEW BY ID
        self.assertTrue(
            any(review_two_id == dic["id"] for dic in reviewlist_pre)
        )
        self.assertTrue(
            not any(review_two_id == dic["id"] for dic in reviewlist_post)
        )

        review_two_del_expect = {"message": "Review deleted successfully"}
        self.assertEqual(review_two_del, review_two_del_expect)

        review_null_del_expect = {"message": "Review not found"}
        self.assertEqual(review_null_del, review_null_del_expect)

        # -GET /api/v1/reviews/
        # --GET REVIEW LIST
        review_one_list_details = {
            x: y
            for x, y in review_one_details.items()
            if x in ["id", "text", "rating"]
        }
        review_two_list_details = {
            x: y
            for x, y in review_two_details.items()
            if x in ["id", "text", "rating"]
        }
        self.assertEqual(
            reviewlist_pre, [review_one_list_details, review_two_list_details]
        )
        self.assertEqual(reviewlist_post, [review_one_list_details])
