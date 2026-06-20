"""api/v1/users api endpoint."""

from flask_restx import Namespace, Resource
from app.services import facade
from app.api.v1.api_models import user_model_full, user_model_input

# Any use of @api.response(<status code>, <string>)
# is for documentation purposes - Seb

# Creates a 'Namespace object' that can be added to the main api object
# passing users to it tells it to represent http://address:port/users
# instead of http://address:port/ for the @api.route() decorator - Seb
api = Namespace("users", description="User operations")


@api.route("/")
class UserList(Resource):
    """API endpoints for creating and listing users."""

    @api.expect(
        user_model_input,
        validate=True,
    )
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered")
    @api.response(400, "Input payload validation failed")
    def post(self) -> tuple:
        """Register a new user.

        Returns:
            Data of created user.

        """
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data["email"])
        if existing_user:
            return {"error": "Email already registered"}, 400

        new_user = facade.create_user(user_data)
        return api.marshal(new_user, user_model_full), 201

    def get(self) -> tuple:
        """Retrive full user list.

        Returns:
            The full list of users.

        """
        users = facade.get_user_list()
        return api.marshal(users, user_model_full), 200


@api.route("/<user_id>")
class UserResource(Resource):
    """API endpoints for getting and updating specific users."""

    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    @api.doc(params={"user_id": "id of user to get"})
    def get(self, user_id: str) -> tuple:
        """Get user details by ID.

        Returns:
            The details of the user with given id.

        """
        user = facade.get_user(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return api.marshal(user, user_model_full), 200

    @api.expect(user_model_input, validate=True)
    @api.response(200, "User successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(404, "User not found")
    @api.doc(params={"user_id": "id of user to update"})
    def put(self, user_id: str) -> tuple:
        """Update user data.

        Returns:
            Updated user data.

        """
        user_data = api.payload
        user = facade.update_user(user_id, user_data)

        if not user:
            return {"error": "User not found"}, 404

        return api.marshal(user, user_model_full), 200
