"""Test users API endpoint."""

import unittest
import shutil

from flask.testing import FlaskClient
from werkzeug.test import TestResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from pprint import pprint
from app import create_app, bcrypt
from app.models.user import User
from test.testconfigs import APIUsersConfigStage


class TestAPIUser(unittest.TestCase):
    """Test for Users api endpoint."""

    def setUp(self) -> None:
        """"""
        self.url = "http://localhost:5000/api/v1"
        self.header = {"Content-Type": "application/json"}
        self.user_one_pass = "upassone"
        self.user_two_pass = "upasstwo"
        self.user_one_email = "John.doe@example.com"
        self.user_two_email = "Jane.doe@example.com"
        shutil.copy(
            "instance/APIUsers.1.db.template", "instance/APIUsers.1.db"
        )
        shutil.copy(
            "instance/APIUsers.2.db.template", "instance/APIUsers.2.db"
        )
        shutil.copy(
            "instance/APIUsers.3.db.template", "instance/APIUsers.3.db"
        )
        shutil.copy(
            "instance/APIUsers.4.db.template", "instance/APIUsers.4.db"
        )

    def test_user_creation(self) -> None:
        """"""
        print("\nRunning test_user_creation. : ", end="")
        from test.testconfigs import APIUsersConfigStage1

        app = create_app(APIUsersConfigStage1())
        client = app.test_client()

        # USERS API TESTS
        user_one_init = {
            "first_name": "John",
            "last_name": "Doe",
            "email": self.user_one_email,
            "password": self.user_one_pass,
        }
        user_two_init = {
            "first_name": "Jake",
            "last_name": "Doe",
            "email": self.user_two_email,
            "password": self.user_two_pass,
        }

        user_badtype_init = {
            "first_name": 3,
            "last_name": True,
            "email": "email.com",
        }
        user_badvalue_init = {
            "first_name": "",
            "last_name": "",
            "email": "j@email.com",
            "password": "3",
        }

        user_repeat_init = user_one_init.copy()

        user_one_json = self.check_response(
            client.post(
                f"{self.url}/users/",
                json=user_one_init,
                headers=self.header,
            ),
            "201 CREATED",
        )

        user_two_json = self.check_response(
            client.post(
                f"{self.url}/users/",
                json=user_two_init,
                headers=self.header,
            ),
            "201 CREATED",
        )
        user_badtype_json = self.check_response(
            client.post(
                f"{self.url}/users/",
                json=user_badtype_init,
                headers=self.header,
            ),
            "400 BAD REQUEST",
        )
        user_badvalue_json = self.check_response(
            client.post(
                f"{self.url}/users/",
                json=user_badvalue_init,
                headers=self.header,
            ),
            "400 BAD REQUEST",
        )

        user_repeat_json = self.check_response(
            client.post(
                f"{self.url}/users/",
                json=user_repeat_init,
                headers=self.header,
            ),
            "400 BAD REQUEST",
        )

        user_one_id = user_one_json["id"]
        user_two_id = user_two_json["id"]

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
        user_badtype_expected = {
            "errors": {
                "first_name": "3 is not of type 'string'",
                "last_name": "True is not of type 'string'",
                "email": "'email.com' does not match '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\\\.[A-Za-z]{2,7}'",
                "password": "'password' is a required property",
            },
            "message": "Input payload validation failed",
        }
        self.assertDictEqual(user_badtype_json, user_badtype_expected)

        user_badvalue_expected = {
            "error": "first name cannot be empty",
        }
        self.assertDictEqual(user_badvalue_json, user_badvalue_expected)

        user_repeat_expected = {"error": "Email already registered"}
        self.assertDictEqual(user_repeat_json, user_repeat_expected)

        # # --GET USER DETAILS BY VALID ID

        user_one_expected = user_one_init.copy()
        user_one_expected["id"] = user_one_id
        user_two_expected = user_two_init.copy()
        user_two_expected["id"] = user_two_id
        with self.configsession(APIUsersConfigStage1()) as session:
            user_one_stored = (
                session.query(User)
                .filter(User.id == user_one_expected["id"])
                .one()
            )
            user_two_stored = (
                session.query(User)
                .filter(User.id == user_two_expected["id"])
                .one()
            )

        user_one_stored_row = {
            k: v
            for k, v in user_one_stored.__dict__.items()
            if k in user_one_expected
        }
        user_two_stored_row = {
            k: v
            for k, v in user_two_stored.__dict__.items()
            if k in user_two_expected
        }

        self.assertTrue(
            bcrypt.check_password_hash(
                user_one_stored_row["password"],
                self.user_one_pass,
            )
        )
        self.assertTrue(
            bcrypt.check_password_hash(
                user_two_stored_row["password"],
                self.user_two_pass,
            )
        )

        del user_one_expected["password"]
        del user_one_stored_row["password"]
        self.assertEqual(user_one_stored_row, user_one_expected)

        del user_two_expected["password"]
        del user_two_stored_row["password"]
        self.assertEqual(user_two_stored_row, user_two_expected)

    def test_user_login(self) -> None:
        """"""
        from test.testconfigs import APIUsersConfigStage2

        print("\nRunning test_login. : ", end="")
        app = create_app(APIUsersConfigStage2)
        client = app.test_client()

        with self.configsession(APIUsersConfigStage2()) as session:
            user_one_stored = (
                session.query(User)
                .filter(User.email == self.user_one_email)  # type: ignore
                .one()
            )
            user_two_stored = (
                session.query(User)
                .filter(User.email == self.user_two_email)  # type: ignore
                .one()
            )

        user_one_stored_row = {
            k: v
            for k, v in user_one_stored.__dict__.items()
            if k in ["id", "first_name", "last_name", "email"]
        }
        user_two_stored_row = {
            k: v
            for k, v in user_two_stored.__dict__.items()
            if k in ["id", "first_name", "last_name", "email"]
        }

        user_one_stored_row["password"] = self.user_one_pass
        user_two_stored_row["password"] = self.user_two_pass

        # USERS API TESTS
        user_one_id = user_one_stored_row["id"]

        # LOGIN API TESTS
        login_one_init = {
            "email": user_one_stored_row["email"],
            "password": user_one_stored_row["password"],
        }

        login_two_init = {
            "email": user_two_stored_row["email"],
            "password": user_two_stored_row["password"],
        }

        login_baduser_init = {
            "email": "dragons@here.be",
            "password": "pass",
        }

        login_badpass_init = {
            "email": user_one_stored_row["email"],
            "password": "weegwerr",
        }

        login_badtype_init = {
            "email": 4,
        }

        login_badvalue_init = {
            "email": "",
            "password": "",
        }

        login_one_json = self.check_response(
            client.post(
                f"{self.url}/auth/login",
                json=login_one_init,
                headers=self.header,
            ),
            "200 OK",
        )

        login_two_json = self.check_response(
            client.post(
                f"{self.url}/auth/login",
                json=login_two_init,
                headers=self.header,
            ),
            "200 OK",
        )

        login_baduser_json = self.check_response(
            client.post(
                f"{self.url}/auth/login",
                json=login_baduser_init,
                headers=self.header,
            ),
            "401 UNAUTHORIZED",
        )

        login_badpass_json = self.check_response(
            client.post(
                f"{self.url}/auth/login",
                json=login_badpass_init,
                headers=self.header,
            ),
            "401 UNAUTHORIZED",
        )

        login_badtype_json = self.check_response(
            client.post(
                f"{self.url}/auth/login",
                json=login_badtype_init,
                headers=self.header,
            ),
            "400 BAD REQUEST",
        )

        login_badvalue_json = self.check_response(
            client.post(
                f"{self.url}/auth/login",
                json=login_badvalue_init,
                headers=self.header,
            ),
            "401 UNAUTHORIZED",
        )

        login_one_jwt = login_one_json["access_token"]
        login_invalid_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc4MzA4OTc0MiwianRpIjoiNGRjZjEwYzktMjg4ZC00MjgyLTliZDktYzY0YzkyN2JiODVmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjU3MWYzMGM3LWFmMWUtNDViYy04ZTgzLTE4YmNhY2YyY2YwYSIsIm5iZiI6MTc4MzA4OTc0MiwiY3NyZiI6IjJiZGZjODRjLTZmYWUtNGFlYi1iNjNhLWFjZTcwNjE2ZDc1MiIsImV4cCI6MTc4MzA5MDY0MiwiaXNfYWRtaW4iOmZhbHNlfQ.PfM4uyCss9OzIWTGtbsOH9-eGgxOC97rZf0jQB8-g3k"

        # ACCESS PROTECTED ROUTES
        protected_one_header = {"Authorization": f"Bearer {login_one_jwt}"}
        protected_invalid_header = {
            "Authorization": f"Bearer {login_invalid_jwt}"
        }

        protected_one_json = self.check_response(
            client.get(
                f"{self.url}/auth/protected",
                headers=protected_one_header,
            ),
            "200 OK",
        )

        protected_invalid_json = self.check_response(
            client.get(
                f"{self.url}/auth/protected",
                headers=protected_invalid_header,
            ),
            "422 UNPROCESSABLE ENTITY",
        )

        protected_null_json = self.check_response(
            client.get(
                f"{self.url}/auth/protected",
            ),
            "401 UNAUTHORIZED",
        )

        # RESPONSE DATA TESTS
        # LOGIN RESPONSE TESTS
        # -POST /api/v1/auth/login/
        # --VALID LOGIN
        self.assertTrue("access_token" in login_one_json.keys())
        self.assertTrue("access_token" in login_two_json.keys())

        # --INVALID LOGIN
        login_baduser_expected = {"error": "Invalid credentials"}
        self.assertEqual(login_baduser_json, login_baduser_expected)
        login_badpass_expected = {"error": "Invalid credentials"}
        self.assertEqual(login_badpass_json, login_badpass_expected)

        login_badtype_expected = {
            "errors": {
                "email": "4 is not of type 'string'",
                "password": "'password' is a required property",
            },
            "message": "Input payload validation failed",
        }
        self.assertEqual(login_badtype_json, login_badtype_expected)

        login_badvalue_expected = {"error": "Invalid credentials"}
        self.assertEqual(login_badvalue_json, login_badvalue_expected)

        # PROTECTED RESPONSE TESTS
        # -GET /api/v1/auth/protected
        # --VALID ACCESS
        protected_one_expected = {"message": f"Hello, user {user_one_id}"}
        self.assertEqual(protected_one_json, protected_one_expected)

        # --INVALID ACCESS

        protected_invalid_expected = {"msg": "Signature verification failed"}
        self.assertEqual(protected_invalid_json, protected_invalid_expected)

        protected_null_expected = {"msg": "Missing Authorization Header"}
        self.assertEqual(protected_null_json, protected_null_expected)
        session.close()

    def test_user_update(self) -> None:
        """"""
        from test.testconfigs import APIUsersConfigStage3

        print("\nRunning test_user_update. : ", end="")
        app = create_app(APIUsersConfigStage3)
        client = app.test_client()

        # Setup Starting data
        with self.configsession(APIUsersConfigStage3()) as session:
            user_one_stored = (
                session.query(User)
                .filter(User.email == self.user_one_email)  # type: ignore
                .one()
            )
            user_two_stored = (
                session.query(User)
                .filter(User.email == self.user_two_email)  # type: ignore
                .one()
            )

        user_one_stored_row = {
            k: v
            for k, v in user_one_stored.__dict__.items()
            if k in ["id", "first_name", "last_name", "email"]
        }
        user_two_stored_row = {
            k: v
            for k, v in user_two_stored.__dict__.items()
            if k in ["id", "first_name", "last_name", "email"]
        }

        user_one_stored_row["password"] = self.user_one_pass
        user_two_stored_row["password"] = self.user_two_pass
        user_one_id = user_one_stored_row["id"]
        user_two_id = user_two_stored_row["id"]
        user_null_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"

        login_one_jwt = self.login(
            self.user_one_email, self.user_one_pass, client
        )
        login_two_jwt = self.login(
            self.user_two_email, self.user_two_pass, client
        )
        protected_one_header = {"Authorization": f"Bearer {login_one_jwt}"}
        protected_two_header = {"Authorization": f"Bearer {login_two_jwt}"}

        # USERS API TESTS
        user_two_update = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": self.user_two_email,
            "password": self.user_two_pass,
        }
        user_twoone_update = {
            "first_name": "Eviljane",
            "last_name": "Doe",
            "email": self.user_one_email,
            "password": self.user_one_pass,
        }
        user_email_update = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "email@change.me",
            "password": self.user_two_pass,
        }
        user_pass_update = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": self.user_two_email,
            "password": "password",
        }
        user_badtype_update = {
            "first_name": 4,
            "last_name": True,
            "email": "nullemail.com",
        }
        user_badvalue_update = {
            "first_name": "helloihaveaveryverylongnamelookitsstillgoinggoodbyee",
            "last_name": "",
            "email": self.user_one_email,
            "password": self.user_one_pass,
        }
        user_null_update = {
            "first_name": "null",
            "last_name": "null",
            "email": "null@email.com",
            "password": "null",
        }

        user_two_updated = self.check_response(
            client.put(
                f"{self.url}/users/{user_two_id}",
                json=user_two_update,
                headers=self.header | protected_two_header,
            ),
            "200 OK",
        )
        user_email_updated = self.check_response(
            client.put(
                f"{self.url}/users/{user_two_id}",
                json=user_email_update,
                headers=self.header | protected_two_header,
            ),
            "400 BAD REQUEST",
        )
        user_pass_updated = self.check_response(
            client.put(
                f"{self.url}/users/{user_two_id}",
                json=user_pass_update,
                headers=self.header | protected_two_header,
            ),
            "400 BAD REQUEST",
        )
        user_nojwt_updated = self.check_response(
            client.put(
                f"{self.url}/users/{user_two_id}",
                json=user_two_update,
                headers=self.header,
            ),
            "401 UNAUTHORIZED",
        )
        user_twoone_updated = self.check_response(
            client.put(
                f"{self.url}/users/{user_one_id}",
                json=user_twoone_update,
                headers=self.header | protected_two_header,
            ),
            "403 FORBIDDEN",
        )
        user_badtype_updated = self.check_response(
            client.put(
                f"{self.url}/users/{user_two_id}",
                json=user_badtype_update,
                headers=self.header,
            ),
            "400 BAD REQUEST",
        )
        user_badvalue_updated = self.check_response(
            client.put(
                f"{self.url}/users/{user_one_id}",
                json=user_badvalue_update,
                headers=self.header | protected_one_header,
            ),
            "400 BAD REQUEST",
        )
        user_null_updated = self.check_response(
            client.put(
                f"{self.url}/users/{user_null_id}",
                json=user_null_update,
                headers=self.header | protected_two_header,
            ),
            "404 NOT FOUND",
        )

        # RESPONSE DATA TESTS
        # --UPDATE USER BY VALID ID
        with self.configsession(APIUsersConfigStage3()) as session:
            user_two_stored_update = (
                session.query(User)
                .filter(
                    User.id == user_two_id  # type: ignore
                )
                .one()
            )
        for key in ["first_name", "last_name", "email"]:
            self.assertEqual(user_two_updated[key], user_two_update[key])
        for key in ["first_name", "last_name", "email"]:
            self.assertEqual(
                user_two_updated[key],
                user_two_stored_update.__dict__[key],
            )

        # --UPDATE USER BY INVALID
        user_twoone_update_expected = {"error": "Unauthorized action."}
        self.assertEqual(user_twoone_updated, user_twoone_update_expected)
        user_nojwt_update_expected = {"msg": "Missing Authorization Header"}
        self.assertEqual(user_nojwt_updated, user_nojwt_update_expected)
        user_badtype_update_expected = {
            "errors": {
                "email": "'nullemail.com' does not match "
                "'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\\\.[A-Za-z]{2,7}'",
                "first_name": "4 is not of type 'string'",
                "last_name": "True is not of type 'string'",
                "password": "'password' is a required property",
            },
            "message": "Input payload validation failed",
        }
        self.assertEqual(user_badtype_updated, user_badtype_update_expected)
        user_badvalue_update_expected = {
            "error": "first name must be no longer then 50 characters"
        }
        self.assertEqual(user_badvalue_updated, user_badvalue_update_expected)
        user_email_update_expected = {"error": "You cannot modify email."}
        self.assertEqual(user_email_updated, user_email_update_expected)
        user_pass_update_expected = {"error": "You cannot modify password."}
        self.assertEqual(user_pass_updated, user_pass_update_expected)
        user_null_update_expected = {"error": "User not found"}
        self.assertEqual(user_null_updated, user_null_update_expected)

    def test_user_details(self) -> None:
        """"""
        from test.testconfigs import APIUsersConfigStage4

        print("\nRunning test_everything. : ", end="")
        app = create_app(APIUsersConfigStage4)
        client = app.test_client()

        with self.configsession(APIUsersConfigStage4()) as session:
            user_one_stored = (
                session.query(User)
                .filter(User.email == self.user_one_email)  # type: ignore
                .one()
            )
            user_two_stored = (
                session.query(User)
                .filter(User.email == self.user_two_email)  # type: ignore
                .one()
            )

        user_one_stored_row = {
            k: v
            for k, v in user_one_stored.__dict__.items()
            if k in ["id", "first_name", "last_name", "email"]
        }
        user_two_stored_row = {
            k: v
            for k, v in user_two_stored.__dict__.items()
            if k in ["id", "first_name", "last_name", "email"]
        }

        user_one_stored_row["password"] = self.user_one_pass
        user_two_stored_row["password"] = self.user_two_pass

        user_one_id = user_one_stored_row["id"]
        user_two_id = user_two_stored_row["id"]
        user_null_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"

        user_two_update = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": self.user_two_email,
            "password": self.user_two_pass,
        }

        # USER API RESUMED
        user_one_details = self.check_response(
            client.get(
                f"{self.url}/users/{user_one_id}",
                headers=self.header,
            ),
            "200 OK",
        )

        user_two_details = self.check_response(
            client.get(
                f"{self.url}/users/{user_two_id}",
                headers=self.header,
            ),
            "200 OK",
        )

        user_null_details = self.check_response(
            client.get(
                f"{self.url}/users/{user_null_id}",
                headers=self.header,
            ),
            "404 NOT FOUND",
        )

        userlist = self.check_response(
            client.get(
                f"{self.url}/users/",
                headers=self.header,
            ),
            "200 OK",
        )
        # RESPONSE DATA TESTS

        # USER RESPONSE TESTS
        # --GET USER DETAILS BY VALID ID
        user_one_details_expected = user_one_stored_row.copy()
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

    ##########################################
    def login(
        self,
        email: str,
        password: str,
        client: FlaskClient,
    ) -> dict:
        """"""
        login_init = {
            "email": email,
            "password": password,
        }
        login_json = self.check_response(
            client.post(
                f"{self.url}/auth/login",
                json=login_init,
                headers=self.header,
            ),
            "200 OK",
        )
        return login_json["access_token"]

    def configsession(self, config: APIUsersConfigStage) -> Session:
        """"""

        engine = create_engine(
            f"{config.SQLALCHEMY_DATABASE_TYPE}/instance/{config.SQLALCHEMY_DATABASE_NAME}"
        )
        return sessionmaker(bind=engine)()

    def check_response(
        self: unittest.TestCase,
        response: TestResponse,
        expected_status: str,
    ) -> dict:
        """"""
        if response.status != expected_status:
            print("###################")
            pprint(response.json)
            pprint(response.status)
            print("###################")
        self.assertEqual(response.status, expected_status)
        if response.json is None:
            raise TypeError("error response.json is None")
        return response.json
