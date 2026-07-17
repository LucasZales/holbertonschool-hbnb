import unittest
from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
import config
from app.services.repositories.user_repository import UserRepository


def check_response(test_case, response, expected_status):
    test_case.assertIn(expected_status, response.status)
    if "204" in expected_status:
        return None
    return response.get_json()


class SystemIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config.DevelopmentConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_full_flow(self):
        url = "/api/v1"
        headers = {"Content-Type": "application/json"}

        # USER API TESTS
        user_one_init = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "securepassword123"
        }
        user_two_init = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "securepassword456"
        }
        user_bad_init = {
            "first_name": "Bad",
            "last_name": "User",
            "email": "invalid-email",
            "password": "123"
        }
        user_two_update = {
            "first_name": "Janet",
            "last_name": "Smith",
            "email": "jane.doe@example.com",
            "password": "securepassword456"
        }
        user_null_update = {
            "first_name": "Ghost",
            "last_name": "User",
            "email": "ghost@example.com"
        }

        user_one_json = check_response(
            self,
            self.client.post(
                f"{url}/users/", json=user_one_init, headers=headers),
            "201 CREATED"
        )
        user_one_id = user_one_json["id"]
        self.assertEqual(user_one_json["id"], user_one_id)
        for key in ["first_name", "last_name", "email"]:
            self.assertEqual(user_one_json[key], user_one_init[key])

        user_two_json = check_response(
            self,
            self.client.post(
                f"{url}/users/", json=user_two_init, headers=headers),
            "201 CREATED"
        )
        user_two_id = user_two_json["id"]
        self.assertEqual(user_two_json["id"], user_two_id)
        for key in ["first_name", "last_name", "email"]:
            self.assertEqual(user_two_json[key], user_two_init[key])

        user_bad_json = check_response(
            self,
            self.client.post(
                f"{url}/users/", json=user_bad_init, headers=headers),
            "400 BAD REQUEST"
        )
        user_bad_expected = {
            "errors": {
                "email": "'invalid-email' does not match '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\\\.[A-Za-z]{2,7}'"
            },
            "message": "Input payload validation failed",
        }
        self.assertDictEqual(user_bad_json, user_bad_expected)

        user_repeat_json = check_response(
            self,
            self.client.post(
                f"{url}/users/", json=user_one_init, headers=headers),
            "409 CONFLICT"
        )
        repo = UserRepository()
        user_check = repo.get(user_two_id)
        login_two_json = check_response(
            self,
            self.client.post(
                f"{url}/auth/login",
                json={
                    "email": "jane.doe@example.com",
                    "password": "securepassword456"
                },
                headers=headers
            ),
            "200 OK"
        )

        token_two = login_two_json["access_token"]
        protected_two_headers = {
            "Authorization": f"Bearer {token_two}"
        }
        user_repeat_expected = {"error": "Email already registered"}
        self.assertDictEqual(user_repeat_json, user_repeat_expected)

        response = self.client.put(
            f"{url}/users/{user_two_id}",
            json=user_two_update,
            headers=headers | protected_two_headers
        )

        response = self.client.get(
            f"{url}/users/{user_two_id}",
            headers=headers
        )
        user_two_updated = check_response(
            self,
            response,
            "200 OK"
        )
        for key in ["first_name", "last_name", "email"]:
            self.assertEqual(user_two_updated[key], user_two_update[key])

        user_null_id = "2fa85f64-5717-4562-b3fc-2c963f66afa6"
        user_null_updated = check_response(
            self,
            self.client.put(f"{url}/users/{user_null_id}",
                            json=user_null_update, headers=headers | protected_two_headers),
            "404 NOT FOUND"
        )
        user_null_update_expected = {"error": "User not found"}
        self.assertEqual(user_null_updated, user_null_update_expected)

        user_one_details = check_response(
            self,
            self.client.get(f"{url}/users/{user_one_id}", headers=headers),
            "200 OK"
        )
        user_one_details_expected = user_one_init.copy()
        user_one_details_expected["id"] = user_one_id
        del user_one_details_expected["password"]
        self.assertEqual(user_one_details, user_one_details_expected)

        user_two_details = check_response(
            self,
            self.client.get(f"{url}/users/{user_two_id}", headers=headers),
            "200 OK"
        )
        user_two_details_expected = user_two_update.copy()
        user_two_details_expected["id"] = user_two_id
        del user_two_details_expected["password"]
        self.assertEqual(user_two_details, user_two_details_expected)

        user_null_details = check_response(
            self,
            self.client.get(f"{url}/users/{user_null_id}", headers=headers),
            "404 NOT FOUND"
        )
        user_null_expected = {"error": "User not found"}
        self.assertEqual(user_null_details, user_null_expected)

        userlist = check_response(
            self,
            self.client.get(f"{url}/users/", headers=headers),
            "200 OK"
        )
        self.assertEqual(userlist, [user_one_details, user_two_details])

        # LOGIN API TESTS
        login_one_init = {
            "email": "john.doe@example.com",
            "password": "securepassword123"
        }
        login_two_init = {
            "email": "jane.doe@example.com",
            "password": "securepassword456"
        }
        login_badpass_init = {
            "email": "john.doe@example.com",
            "password": "wrongpassword"
        }
        login_baddata_init = {
            "email": "john.doe@example.com",
            "password": 4
        }
        login_null_init = {
            "email": "nobody@example.com",
            "password": "somepassword"
        }

        login_one_json = check_response(
            self,
            self.client.post(f"{url}/auth/login",
                             json=login_one_init, headers=headers),
            "200 OK"
        )
        self.assertTrue("access_token" in login_one_json.keys())
        token_one = login_one_json.get("access_token", "")

        login_two_json = check_response(
            self,
            self.client.post(f"{url}/auth/login",
                             json=login_two_init, headers=headers),
            "200 OK"
        )
        self.assertTrue("access_token" in login_two_json.keys())
        token_two = login_two_json.get("access_token", "")

        protected_one_headers = {"Authorization": f"Bearer {token_one}"}
        protected_two_headers = {"Authorization": f"Bearer {token_two}"}
        protected_invalid_headers = {"Authorization": "Bearer invalidtoken123"}

        login_badpass_json = check_response(
            self,
            self.client.post(f"{url}/auth/login",
                             json=login_badpass_init, headers=headers),
            "401 UNAUTHORIZED"
        )
        login_badpass_expected = {"error": "Invalid credentials"}
        self.assertEqual(login_badpass_json, login_badpass_expected)

        login_baddata_json = check_response(
            self,
            self.client.post(f"{url}/auth/login",
                             json=login_baddata_init, headers=headers),
            "400 BAD REQUEST"
        )
        login_baddata_expected = {
            "errors": {"password": "4 is not of type 'string'"},
            "message": "Input payload validation failed",
        }
        self.assertEqual(login_baddata_json, login_baddata_expected)

        login_null_json = check_response(
            self,
            self.client.post(f"{url}/auth/login",
                             json=login_null_init, headers=headers),
            "401 UNAUTHORIZED"
        )
        login_null_expected = {"error": "Invalid credentials"}
        self.assertEqual(login_null_json, login_null_expected)

        protected_one_json = check_response(
            self,
            self.client.get(f"{url}/auth/protected",
                            headers=headers | protected_one_headers),
            "200 OK"
        )
        protected_one_expected = {"message": f"Hello, user {user_one_id}"}
        self.assertEqual(protected_one_json, protected_one_expected)

        protected_invalid_json = check_response(
            self,
            self.client.get(f"{url}/auth/protected",
                            headers=headers | protected_invalid_headers),
            "401 UNAUTHORIZED"
        )
        protected_invalid_expected = {"msg": "Signature verification failed"}
        self.assertEqual(protected_invalid_json, protected_invalid_expected)

        protected_null_json = check_response(
            self,
            self.client.get(f"{url}/auth/protected", headers=headers),
            "401 UNAUTHORIZED"
        )
        protected_null_expected = {"msg": "Missing Authorization Header"}
        self.assertEqual(protected_null_json, protected_null_expected)

        # AMENITY API TESTS
        amenity_one_init = {"name": "WiFi"}
        amenity_two_init = {"name": "Pool"}
        amenity_bad_init = {"name": ""}
        amenity_two_update = {"name": "Swimming Pool"}
        amenity_null_update = {"name": "Gym"}

        response = self.client.post(f"{url}/amenities/", json=amenity_one_init,
                                    headers=headers | protected_one_headers)

        print("AMEN STAT:", response.status)
        print("AMEN BOD:", response.get_json())
        amenity_one_json = check_response(self, response, "201 CREATED")

        amenity_one_id = amenity_one_json["id"]
        amenity_one_expected = amenity_one_init.copy()
        amenity_one_expected["id"] = amenity_one_id
        self.assertEqual(amenity_one_json, amenity_one_expected)

        amenity_two_json = check_response(
            self,
            self.client.post(f"{url}/amenities/", json=amenity_two_init,
                             headers=headers | protected_one_headers),
            "201 CREATED"
        )
        amenity_two_id = amenity_two_json["id"]
        amenity_two_expected = amenity_two_init.copy()
        amenity_two_expected["id"] = amenity_two_id
        self.assertEqual(amenity_two_json, amenity_two_expected)

        amenity_bad_json = check_response(
            self,
            self.client.post(f"{url}/amenities/", json=amenity_bad_init,
                             headers=headers | protected_one_headers),
            "400 BAD REQUEST"
        )
        amenity_bad_expected = {"error": "Name cannot be empty"}
        self.assertDictEqual(amenity_bad_json, amenity_bad_expected)

        amenity_two_updated = check_response(
            self,
            self.client.put(f"{url}/amenities/{amenity_two_id}",
                            json=amenity_two_update, headers=headers),
            "200 OK"
        )
        amenity_two_update_expected = {
            "message": "Amenity updated successfully"}
        self.assertEqual(amenity_two_updated, amenity_two_update_expected)

        amenity_null_id = "2fa85f64-5717-4562-b3fc-2c963f66afa6"
        amenity_null_updated = check_response(
            self,
            self.client.put(f"{url}/amenities/{amenity_null_id}",
                            json=amenity_null_update, headers=headers),
            "404 NOT FOUND"
        )
        amenity_null_update_expected = {"error": "Amenity not found"}
        self.assertEqual(amenity_null_updated,
                         amenity_null_update_expected)

        amenity_one_details = check_response(
            self,
            self.client.get(
                f"{url}/amenities/{amenity_one_id}", headers=headers),
            "200 OK"
        )
        amenity_one_details_expected = amenity_one_init.copy()
        amenity_one_details_expected["id"] = amenity_one_id
        self.assertEqual(amenity_one_details, amenity_one_details_expected)

        amenity_two_details = check_response(
            self,
            self.client.get(
                f"{url}/amenities/{amenity_two_id}", headers=headers),
            "200 OK"
        )
        amenity_two_details_expected = amenity_two_update.copy()
        amenity_two_details_expected["id"] = amenity_two_id
        self.assertEqual(amenity_two_details, amenity_two_details_expected)

        amenity_null_details = check_response(
            self,
            self.client.get(
                f"{url}/amenities/{amenity_null_id}", headers=headers),
            "404 NOT FOUND"
        )
        amenity_null_expected = {"error": "Amenity not found"}
        self.assertEqual(amenity_null_details, amenity_null_expected)

        amenitylist = check_response(
            self,
            self.client.get(f"{url}/amenities/", headers=headers),
            "200 OK"
        )
        self.assertEqual(
            amenitylist, [amenity_one_details, amenity_two_details])

        # PLACE API TESTS
        place_one_init = {
            "title": "Cozy Cabin",
            "description": "A nice cabin in the woods",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -45.0,
            "owner_id": user_one_id
        }
        place_two_init = {
            "title": "Beachside Condo",
            "description": "Beautiful condo next to the beach",
            "price": 200.0,
            "latitude": 30.0,
            "longitude": -30.0,
            "owner_id": user_two_id
        }
        place_bad_init = {
            "title": "Broken House",
            "description": "No owner house",
            "price": 50.0,
            "latitude": 0.0,
            "longitude": 0.0,
            "owner_id": user_null_id
        }
        place_two_update = {
            "title": "Luxury Beachside Condo",
            "description": "Renovated luxury condo next to the beach",
            "price": 250.0,
            "latitude": 30.0,
            "longitude": -30.0
        }
        place_null_update = {
            "title": "Haunted Mansion",
            "description": "Does not exist",
            "price": 666.0,
            "latitude": 13.0,
            "longitude": -13.0
        }

        place_one_json = check_response(
            self,
            self.client.post(f"{url}/places/", json=place_one_init,
                             headers=headers | protected_one_headers),
            "201 CREATED"
        )
        place_one_id = place_one_json["id"]
        place_one_expected = place_one_init.copy()
        place_one_expected["id"] = place_one_id
        self.assertEqual(place_one_json, place_one_expected)

        place_two_json = check_response(
            self,
            self.client.post(f"{url}/places/", json=place_two_init,
                             headers=headers | protected_two_headers),
            "201 CREATED"
        )
        place_two_id = place_two_json["id"]
        place_two_expected = place_two_init.copy()
        place_two_expected["id"] = place_two_id
        self.assertEqual(place_two_json, place_two_expected)

        place_bad_json = check_response(
            self,
            self.client.post(f"{url}/places/", json=place_bad_init,
                             headers=headers | protected_one_headers),
            "404 NOT FOUND"
        )
        place_bad_expected = {"error": "Owner not found"}
        self.assertDictEqual(place_bad_json, place_bad_expected)

        place_two_updated = check_response(
            self,
            self.client.put(f"{url}/places/{place_two_id}",
                            json=place_two_update, headers=headers | protected_two_headers),
            "200 OK"
        )
        place_two_update_expected = {
            "message": "Place updated successfully"}
        self.assertEqual(place_two_updated, place_two_update_expected)

        place_null_id = "2fa85f64-5717-4562-b3fc-2c963f66afa6"
        place_null_updated = check_response(
            self,
            self.client.put(f"{url}/places/{place_null_id}",
                            json=place_null_update, headers=headers | protected_two_headers),
            "404 NOT FOUND"
        )
        place_null_update_expected = {"error": "Place not found"}
        self.assertEqual(place_null_updated, place_null_update_expected)

        place_one_details = check_response(
            self,
            self.client.get(f"{url}/places/{place_one_id}", headers=headers),
            "200 OK"
        )
        place_one_details_expected = place_one_init.copy()
        place_one_details_expected["id"] = place_one_id
        place_one_details_expected["amenities"] = []
        place_one_details_expected["owner"] = user_one_details
        place_one_details_expected.pop("owner_id", None)
        self.assertEqual(place_one_details, place_one_details_expected)

        place_two_details = check_response(
            self,
            self.client.get(f"{url}/places/{place_two_id}", headers=headers),
            "200 OK"
        )
        place_two_details_expected = place_two_update.copy()
        place_two_details_expected["id"] = place_two_id
        place_two_details_expected["amenities"] = []
        place_two_details_expected["owner"] = user_two_details
        place_two_details_expected.pop("owner_id", None)
        self.assertEqual(place_two_details, place_two_details_expected)

        place_null_details = check_response(
            self,
            self.client.get(f"{url}/places/{place_null_id}", headers=headers),
            "404 NOT FOUND"
        )
        place_null_expected = {"error": "Place not found"}
        self.assertEqual(place_null_details, place_null_expected)

        placelist = check_response(
            self,
            self.client.get(f"{url}/places/", headers=headers),
            "200 OK"
        )
        place_one_list_details = {x: y for x, y in place_one_details.items() if x in [
            "id", "title", "latitude", "longitude"]}
        place_two_list_details = {x: y for x, y in place_two_details.items() if x in [
            "id", "title", "latitude", "longitude"]}
        self.assertEqual(
            placelist, [place_one_list_details, place_two_list_details])

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
        review_badtype_init = {
            "text": 42,
            "rating": 30,
            "user_id": user_null_id,
            "place_id": place_null_id,
        }
        review_badvalue_init = {
            "text": "",
            "rating": 30,
            "user_id": user_two_id,
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
            self.client.post(f"{url}/reviews/", json=review_one_init,
                             headers=headers | protected_one_headers),
            "201 CREATED",
        )
        review_one_id = review_one_json["id"]
        review_one_expected = review_one_init.copy()
        review_one_expected["id"] = review_one_id
        self.assertEqual(review_one_json, review_one_expected)

        review_two_json = check_response(
            self,
            self.client.post(f"{url}/reviews/", json=review_two_init,
                             headers=headers | protected_two_headers),
            "201 CREATED",
        )
        review_two_id = review_two_json["id"]
        review_two_expected = review_two_init.copy()
        review_two_expected["id"] = review_two_id
        self.assertEqual(review_two_json, review_two_expected)

        review_badtype_json = check_response(
            self,
            self.client.post(f"{url}/reviews/",
                             json=review_badtype_init, headers=headers),
            "400 BAD REQUEST",
        )
        review_badtype_expected = {
            "errors": {"text": "42 is not of type 'string'"},
            "message": "Input payload validation failed",
        }
        self.assertDictEqual(review_badtype_json, review_badtype_expected)

        review_badvalue_json = check_response(
            self,
            self.client.post(f"{url}/reviews/", json=review_badvalue_init,
                             headers=headers | protected_two_headers),
            "404 NOT FOUND",
        )
        review_badvalue_expected = {"error": "Place not found"}
        self.assertDictEqual(review_badvalue_json,
                             review_badvalue_expected)

        review_two_updated = check_response(
            self,
            self.client.put(f"{url}/reviews/{review_two_id}",
                            json=review_two_update, headers=headers | protected_two_headers),
            "200 OK",
        )
        review_two_update_expected = {
            "message": "Review updated successfully"}
        self.assertEqual(review_two_updated, review_two_update_expected)

        review_null_id = "2fa85f64-5717-4562-b3fc-2c963f66afa6"
        review_null_updated = check_response(
            self,
            self.client.put(f"{url}/reviews/{review_null_id}",
                            json=review_null_update, headers=headers | protected_two_headers),
            "404 NOT FOUND",
        )
        review_null_update_expected = {"error": "Review not found"}
        self.assertEqual(review_null_updated, review_null_update_expected)

        review_one_details = check_response(
            self,
            self.client.get(f"{url}/reviews/{review_one_id}", headers=headers),
            "200 OK",
        )
        review_one_details_expected = review_one_init.copy()
        review_one_details_expected["id"] = review_one_id
        self.assertEqual(review_one_details, review_one_details_expected)

        review_two_details = check_response(
            self,
            self.client.get(f"{url}/reviews/{review_two_id}", headers=headers),
            "200 OK",
        )
        review_two_details_expected = review_two_update.copy()
        review_two_details_expected["id"] = review_two_id
        review_two_details_expected["user_id"] = user_two_id
        review_two_details_expected["place_id"] = place_one_id
        self.assertEqual(review_two_details, review_two_details_expected)

        review_null_details = check_response(
            self,
            self.client.get(
                f"{url}/reviews/{review_null_id}", headers=headers),
            "404 NOT FOUND"
        )
        review_null_expected = {"error": "Review not found"}
        self.assertEqual(review_null_details, review_null_expected)

        # -- GET REVIEW LIST (PRE-DELETE)
        reviewlist_pre = check_response(
            self,
            self.client.get(f"{url}/reviews/", headers=headers),
            "200 OK",
        )
        review_one_list_details = {x: y for x, y in review_one_details.items() if x in [
            "id", "text", "rating"]}
        review_two_list_details = {x: y for x, y in review_two_details.items() if x in [
            "id", "text", "rating"]}
        self.assertEqual(reviewlist_pre, [
            review_one_list_details, review_two_list_details])

        # -- DELETE REVIEW BY ID
        review_two_del = check_response(
            self,
            self.client.delete(f"{url}/reviews/{review_two_id}",
                               headers=headers | protected_two_headers),
            "200 OK",)
        review_two_del_expect = {"message": "Review deleted successfully"}
        self.assertEqual(review_two_del, review_two_del_expect)

        review_null_del = check_response(
            self,
            self.client.delete(f"{url}/reviews/{review_null_id}",
                               headers=headers | protected_two_headers),
            "404 NOT FOUND",
        )
        review_null_del_expect = {"error": "Review not found"}
        self.assertEqual(review_null_del, review_null_del_expect)

        # -- GET REVIEW LIST (POST-DELETE)
        reviewlist_post = check_response(
            self,
            self.client.get(f"{url}/reviews/", headers=headers),
            "200 OK",
        )
        self.assertTrue(
            any(review_two_id == dic["id"] for dic in reviewlist_pre))
        self.assertTrue(
            not any(review_two_id == dic["id"] for dic in reviewlist_post))
        self.assertEqual(reviewlist_post, [review_one_list_details])

        # -- GET ALL REVIEWS FOR A SPECIFIC PLACE
        place_one_reviews = check_response(
            self,
            self.client.get(
                f"{url}/places/{place_one_id}/reviews", headers=headers),
            "200 OK",
        )
        place_one_reviews_expected = []
        self.assertEqual(place_one_reviews, place_one_reviews_expected)

        place_two_reviews = check_response(
            self,
            self.client.get(
                f"{url}/places/{place_two_id}/reviews", headers=headers),
            "200 OK",
        )
        place_two_reviews_expected = [
            {k: v for k, v in review_one_details.items() if k in ["id", "text", "rating"]}]
        self.assertEqual(place_two_reviews, place_two_reviews_expected)

        place_null_reviews = check_response(
            self,
            self.client.get(
                f"{url}/places/{place_null_id}/reviews", headers=headers),
            "404 NOT FOUND",
        )
        place_null_reviews_expected = {"error": "Place not found"}
        self.assertEqual(place_null_reviews, place_null_reviews_expected)

        if __name__ == "__main__":
            unittest.main()
