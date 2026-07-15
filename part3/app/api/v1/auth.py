"""api/v1/login api endpoint."""

from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from app.exception.notfound import NotFoundError, NotAuthorizedError
from app.services import facade
from app.api.v1.api_models import login_model

api = Namespace("auth", description="Authentication operations")


@api.route("/login")
class Login(Resource):
    """API endpoint for logging in."""

    @api.expect(
        login_model,
        validate=True,
    )
    def post(self) -> tuple:
        """Authenticate user and return a JWT token.

        Returns:
            Success status of login and potential jwt

        """
        credentials = (
            api.payload
        )  # Get the email and password from the request payload

        # Step 1: Retrieve the user based on the provided email
        try:
            user = facade.get_user_by_email(credentials["email"])
        except NotFoundError:
            return {"error": "Invalid credentials"}, 401

        # Step 2: Check if the user exists and the password is correct
        if not user.verify_password(credentials["password"]):
            return {"error": "Invalid credentials"}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin},
        )

        # Step 4: Return the JWT token to the client
        return {"access_token": access_token}, 200


@api.route("/protected")
class ProtectedResource(Resource):
    """Example Protected API endpoint for testing purposes."""

    @jwt_required()
    def get(self) -> tuple:
        """Protected endpoint that requires a valid JWT token.

        Returns:
            ...

        """
        current_user = (
            get_jwt_identity()
        )  # Retrieve the user's identity from the token
        # if you need to see if the user is an admin or not, you can access
        # additional claims using get_jwt() :
        # addtional claims = get_jwt()
        # additional claims["is_admin"] -> True or False
        return {"message": f"Hello, user {current_user}"}, 200


def jwt_authorise(get_object):
    """Decorator to Verify Ownership"""
    def decorator(func):
        @wraps(func)
        @jwt_required
        def authorise(object_id, *args, **kwargs):
            obj = get_object(object_id)
            if obj is None:
                raise NotFoundError()
            owner_id = getattr(obj, "owner_id", None)
            if owner_id is None:
                owner_id = obj.user_id
            if not get_jwt()["is_admin"] and get_jwt_identity() != owner_id:
                raise NotAuthorizedError("Unauthorized action.")
            return func(obj, *args, **kwargs)
        return authorise
    return decorator
