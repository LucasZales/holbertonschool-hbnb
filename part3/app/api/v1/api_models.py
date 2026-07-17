"""Module for api models."""

from flask_restx import Namespace, fields

api = Namespace("Models", description="Model deffinitions")

# USER API MODELS
user_model_base = api.model(
    "User_Base",
    {
        "first_name": fields.String(
            required=True,
            description="First name of the user",
            example="John",
        ),
        "last_name": fields.String(
            required=True,
            description="Last name of the user",
            example="Doe",
        ),
        "email": fields.String(
            required=True,
            description="Email of the user",
            example="john.doe@example.com",
            pattern=r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}",
        ),
    },
)
user_model_input = api.inherit(
    "User_Input",
    user_model_base,
    {
        "password": fields.String(
            required=True,
            description="Password of the user",
            example="securepassword123",
        ),
    },
)
user_model_update = api.model(
    "UserUpdate",
    {
        "first_name": fields.String,
        "last_name": fields.String,
        "email": fields.String,
        "password": fields.String,
    }
)
user_model_full = api.inherit(
    "User_Full",
    user_model_base,
    {
        "id": fields.String(
            required=False,
            description="id of the user",
            example="1e408ff9-e4c3-4a31-9058-089a94494c99",
        ),
    },
)


# AMENITY API MODELS
amenity_model = api.model(
    "Amenity",
    {"name": fields.String(required=True, description="Name of the amenity")},
)

amenity_model_place = api.inherit(
    "PlaceAmenity",
    amenity_model,
    {
        "id": fields.String(description="Amenity ID"),
    },
)

# REVIEW API MODELS
review_model_base = api.model(
    "Review_base",
    {
        "text": fields.String(required=True, description="Text of the review"),
        "rating": fields.Integer(required=True, description="Rating (1-5)"),
        "user_id": fields.String(required=True, description="User ID"),
    },
)
review_model_creation = api.inherit(
    "Review_creation",
    review_model_base,
    {
        "place_id": fields.String(required=True, description="Place ID"),
    },
)
review_model_full = api.inherit(
    "Review_full",
    review_model_base,
    {
        "place_id": fields.String(required=True, description="Place ID"),
        "id": fields.String(description="Review ID"),
    },
)
review_model_place = api.inherit(
    "Review_place",
    review_model_base,
    {
        "id": fields.String(description="Review ID"),
    },
)

# PLACE API MODELS
place_model_base = api.model(
    "Place_model_base",
    {
        "title": fields.String(
            required=True, description="Title of the place"
        ),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(required=True, description="Price per night"),
        "latitude": fields.Float(
            required=True, description="Latitude of the place"
        ),
        "longitude": fields.Float(
            required=True, description="Longitude of the place"
        ),
        "owner_id": fields.String(
            required=True, description="ID of the owner"
        ),
    },
)
place_model = api.inherit(
    "Place_model",
    place_model_base,
    {
        "owner": fields.Nested(
            user_model_full,
            description="Owner of the place",
        ),
        "amenities": fields.List(
            fields.Nested(amenity_model),
            description="List of amenities",
        ),
        "reviews": fields.List(
            fields.Nested(review_model_place),
            description="List of reviews",
        ),
    },
)
# LOGIN MODEL
login_model = api.model(
    "Login",
    {
        "email": fields.String(required=True, description="User email"),
        "password": fields.String(required=True, description="User password"),
    },
)
place_model_full = api.inherit(
    "Place_model_full",
    place_model,
    {
        "id": fields.String(
            required=False,
            description="id of the place",
            example="1e408ff9-e4c3-4a31-9058-089a94494c99",
        ),
    },
)
place_model_return = api.inherit(
    "Place_model_return",
    place_model_base,
    {
        "id": fields.String(
            required=False,
            description="id of the place",
            example="1e408ff9-e4c3-4a31-9058-089a94494c99",
        ),
    },
)
