"""api/v1/places api endpoint."""

from flask_restx import Namespace, Resource
from app.exception.notfound import NotFoundError
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.api.v1.auth import jwt_authorise
from app.api.v1.api_models import (
    place_model,
    place_model_return,
    review_model_place,
    place_model_full,
)

api = Namespace("places", description="Place operations")


@api.route("/")
class PlaceList(Resource):
    """API endpoints for creating and listing places."""

    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @jwt_required()
    def post(self) -> tuple:
        """Register a new place.

        Returns:
                                Data of created place.

        """
        place_data = api.payload.copy()
        place_data["owner_id"] = get_jwt_identity()

        try:
            new_place = facade.create_place(place_data)
        except NotFoundError as e:
            return {"error": str(e)}, 404
        except ValueError as e:
            return {"error": str(e)}, 400

        return api.marshal(new_place, place_model_return), 201

    @api.response(200, "List of places retrieved successfully")
    def get(self) -> tuple:
        """Retrieve full list of places.

        Returns:
                                A list of all places.

        """
        places = facade.get_all_places()

        return api.marshal(
            places, place_model_return, mask="{id,title,latitude,longitude}"
        ), 200


@api.route("/<place_id>")
class PlaceResource(Resource):
    """API endpoints for getting and updating specific places."""

    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id: str) -> tuple:
        """Get place details by ID.

        Returns:
                                Detailes of place with given id.

        """
        try:
            place = facade.get_place(place_id)
        except NotFoundError as e:
            return {"error": str(e)}, 404

        return api.marshal(
            place,
            place_model_full,
            mask="{id,title,description,price,latitude,longitude,owner,amenities}",
        )

    @api.expect(place_model, validate=True)
    @api.response(200, "Place successfully updated")
    @api.response(404, "Place not found")
    @api.response(400, "Invalid input data")
    @jwt_authorise(facade.get_place)
    def put(self, place_id: str) -> tuple:
        """Update place data.

        Returns:
                                Updated data of place.

        """
        place_data = api.payload

        try:
            facade.update_place(place_id, place_data)
        except NotFoundError as e:
            return {"error": str(e)}, 404
        except ValueError as e:
            return {"error": str(e)}, 400

        return {"message": "Place updated successfully"}, 200

    @jwt_authorise(facade.get_place)
    def delete(self, place_id: str) -> tuple:
        """Delete Place

          Returns:
                                          Success or failure of Place Deletion
          """
        try:
            facade.delete_place(place_id)
        except NotFoundError as e:
            return {"error": str(e)}, 404
        return {"message": "Place deleted successfully"}, 200


# endpoint for reviews
@api.route("/<place_id>/reviews")
class PlaceReviewList(Resource):
    """API endpoint for listing rreviews of a place."""

    def get(self, place_id: str) -> tuple:
        """Get all reviews for a place.

        Returns:
                                List of review for given place.

        """
        try:
            reviews = facade.get_reviews_by_place(place_id)
        except NotFoundError as e:
            return {"error": str(e)}, 404

        return api.marshal(
            reviews, review_model_place, mask="{id,text,rating}"
        ), 200
