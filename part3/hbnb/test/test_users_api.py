"""Test for User class."""

import unittest
import requests
import json


def create_new_user(url: str, data: dict) -> None:
    """Create a new user with post request to /api/v1/users."""
    headers = {"Content-Type": "application/json"}
    good_expected = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
    }
    good_reason = "CREATED"
    good_status = 201
    good_id_len = 36
    good_request = requests.post(
        url,
        data=json.dumps(data),
        headers=headers,
        timeout=5,
    )
    good_response = json.loads(good_request.text)
    return good_response["id"]


class TestUsersAPI(unittest.TestCase):
    """Test for users api endpoint."""

    url = "http://localhost:5000/api/v1/users/"

    # def base(self) -> None:
    #     """."""
    #     print("Running .")
    #     headers = {"Content-Type": "application/json"}
    #     _expected = {}
    #     _reason = ""
    #     _status = 0
    #     _request = requests.get(str(""), headers={"": ""}, timeout=5)
    #     _response = json.loads(_request.text)
    #     self.assertEqual(_request.status_code, _status)
    #     self.assertEqual(_request.reason, _reason)
    #     self.assertEqual(
    #         _response[""],
    #         _expected[""],
    #     )

    def test_new_user_creation(self) -> None:
        """Test creation of user with post request to /api/v1/users."""
        print("Running test_new_user_creation.")
        headers = {"Content-Type": "application/json"}
        good_json = '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
        good_expected = {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
        }
        good_reason = "CREATED"
        good_status = 201
        good_id_len = 36
        good_request = requests.post(
            self.url, data=good_json, headers=headers, timeout=5
        )
        good_response = json.loads(good_request.text)
        self.assertEqual(good_request.status_code, good_status)
        self.assertEqual(good_request.reason, good_reason)
        self.assertEqual(len(good_response["id"]), good_id_len)
        self.assertEqual(
            good_response["first_name"], good_expected["first_name"]
        )
        self.assertEqual(
            good_response["last_name"], good_expected["last_name"]
        )
        self.assertEqual(good_response["email"], good_expected["email"])

        # Test repeat for already exists err
        repeat_json = '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
        repeat_expected = {"error": "Email already registered"}
        repeat_reason = "BAD REQUEST"
        repeat_status = 400
        repeat_request = requests.post(
            self.url, data=repeat_json, headers=headers, timeout=5
        )
        repeat_response = json.loads(repeat_request.text)
        self.assertEqual(repeat_request.status_code, repeat_status)
        self.assertEqual(repeat_request.reason, repeat_reason)
        self.assertEqual(repeat_response, repeat_expected)

    def test_bad_input(self) -> None:
        """Test post request with bad input to /api/v1/users."""
        print("Running test_bad_input.")
        headers = {"Content-Type": "application/json"}
        bad_json = '{"first_name": 1, "last_name": {"hello":"three"}, "email": "john.doeexample.com"}'
        bad_request = requests.post(
            self.url, data=bad_json, headers=headers, timeout=5
        )
        bad_response = json.loads(bad_request.text)
        bad_expected = {
            "errors": {
                "first_name": "1 is not of type 'string'",
                "last_name": "{'hello': 'three'} is not of type 'string'",
                "email": "'john.doeexample.com' does not match '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\\\.[A-Za-z]{2,7}'",
            },
            "message": "Input payload validation failed",
        }
        bad_reason = "BAD REQUEST"
        bad_status = 400

        self.assertEqual(bad_request.status_code, bad_status)
        self.assertEqual(bad_request.reason, bad_reason)
        self.assertEqual(
            bad_response["errors"],
            bad_expected["errors"],
        )
        self.assertEqual(
            bad_response["errors"]["first_name"],
            bad_expected["errors"]["first_name"],
        )
        self.assertEqual(
            bad_response["errors"]["last_name"],
            bad_expected["errors"]["last_name"],
        )
        self.assertEqual(
            bad_response["errors"]["email"],
            bad_expected["errors"]["email"],
        )
        self.assertEqual(
            bad_response["message"],
            bad_expected["message"],
        )

    def test_retrive_user_by_id(self) -> None:
        """Test retriving users with both valid and invalud id's."""
        print("Running test_retrive_user_by_id.")
        headers = {"Content-Type": "application/json"}
        new_user_json = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
        }
        request = requests.post(
            self.url,
            data=json.dumps(new_user_json),
            headers=headers,
            timeout=5,
        )
        response = json.loads(request.text)
        good_id = response["id"]
        good_expected = {
            "id": good_id,
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
        }
        good_reason = "OK"
        good_status = 200
        good_request = requests.get(
            str(f"{self.url}{good_id}"), headers=headers, timeout=5
        )
        good_response = json.loads(good_request.text)
        self.assertEqual(good_request.status_code, good_status)
        self.assertEqual(good_request.reason, good_reason)
        self.assertEqual(
            good_response["id"],
            good_expected["id"],
        )
        self.assertEqual(
            good_response["first_name"],
            good_expected["first_name"],
        )
        self.assertEqual(
            good_response["last_name"],
            good_expected["last_name"],
        )
        self.assertEqual(
            good_response["email"],
            good_expected["email"],
        )

        bad_id = "44006f8-779f-45fd-b477-0f5ef96ba841"
        bad_expected = {"error": "User not found"}
        bad_reason = "NOT FOUND"
        bad_status = 404
        bad_request = requests.get(
            str(f"{self.url}{bad_id}"), headers=headers, timeout=5
        )
        bad_response = json.loads(bad_request.text)
        self.assertEqual(bad_request.status_code, bad_status)
        self.assertEqual(bad_request.reason, bad_reason)
        self.assertEqual(bad_response, bad_expected)

    def test_get_user_list(self) -> None:
        """Test retriving all users."""
        print("Running test_get_user_list.")
        headers = {"Content-Type": "application/json"}
        good_reason = "OK"
        good_status = 200
        good_request = requests.get(self.url, headers=headers, timeout=5)
        self.assertEqual(good_request.status_code, good_status)
        self.assertEqual(good_request.reason, good_reason)
        self.assertIsInstance(good_request.json(), list)

    def test_update_user(self) -> None:
        """Test updating user."""
        print("Running test_update_user.")
        headers = {"Content-Type": "application/json"}
        user_data_1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "John.doe@example.com",
        }
        user_data_2 = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
        }
        good_id = create_new_user(self.url, user_data_1)
        bad_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        good_expected = {
            "id": good_id,
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
        }
        bad_expected = {"error": "User not found"}
        good_reason = "OK"
        good_status = 200
        bad_reason = "NOT FOUND"
        bad_status = 404
        good_request = requests.put(
            str(f"{self.url}{good_id}"),
            data=json.dumps(user_data_2),
            headers=headers,
            timeout=5,
        )
        good_response = json.loads(good_request.text)
        bad_request = requests.put(
            str(f"{self.url}{bad_id}"),
            data=json.dumps(user_data_2),
            headers=headers,
            timeout=5,
        )
        bad_response = json.loads(bad_request.text)
        self.assertEqual(good_request.status_code, good_status)
        self.assertEqual(good_request.reason, good_reason)
        self.assertEqual(
            good_response["id"],
            good_expected["id"],
        )
        self.assertEqual(
            good_response["first_name"],
            good_expected["first_name"],
        )
        self.assertEqual(
            good_response["last_name"],
            good_expected["last_name"],
        )
        self.assertEqual(
            good_response["email"],
            good_expected["email"],
        )
        self.assertEqual(bad_request.status_code, bad_status)
        self.assertEqual(bad_request.reason, bad_reason)
        self.assertEqual(
            bad_response,
            bad_expected,
        )
