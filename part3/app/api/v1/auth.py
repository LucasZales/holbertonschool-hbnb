from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from functools import wraps
from flask import g
from app.exception.notfound import NotFoundError
from app.exception.notauthorized import NotAuthorizedError
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
        credentials = api.payload

        print("LOGIN EMAIL:", credentials["email"])
        print("LOGIN PASSWORD:", credentials["password"])

        # Step 1: Retrieve the user based on the provided email
        try:
            user = facade.get_user_by_email(credentials["email"])
        except NotFoundError:
            print("USER NOT FOUND")
            return {"error": "Invalid credentials"}, 401

        print("FOUND USER:", user.email)
        print("FOUND HASH:", user.password)
        print("VERIFY RESULT:", user.verify_password(
            credentials["password"]))

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
        @jwt_required()
        def authorise(self, *args, **kwargs):
            object_id = kwargs.get("place_id") or kwargs.get(
                "user_id") or kwargs.get("review_id") or kwargs.get("amenity_id")
            if not object_id and args:
                object_id = args[0]

            try:
                obj = get_object(object_id)
            except NotFoundError as e:
                return {"error": str(e)}, 404

            if obj is None:
                return {"error": "Resource not found."}, 404

            if hasattr(obj, "owner_id"):
                owner_id = obj.owner_id
            elif hasattr(obj, "user_id"):
                owner_id = obj.user_id
            else:
                owner_id = obj.id
            current_identity = str(get_jwt_identity())
            owner_identity = str(owner_id)
            is_admin = get_jwt().get("is_admin", False)
            if not is_admin and current_identity != owner_identity:
                return {"error": "Unauthorized action."}, 403
            g.validated_obj = obj
            return func(self, *args, **kwargs)
        return authorise
    return decorator
