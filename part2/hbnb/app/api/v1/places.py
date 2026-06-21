"""api/v1/places api endpoint."""

from flask_restx import Namespace, Resource
from app.services import facade
from app.api.v1.api_models import (
    place_model,
)

api = Namespace("places", description="Place operations")


@api.route("/")
class PlaceList(Resource):
    """API endpoints for creating and listing places."""

    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    def post(self) -> tuple:
        """Register a new place.

        Returns:
            Data of created place.

        """
        place_data = api.payload

        try:
            new_place = facade.create_place(place_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return {
            "id": new_place.id,
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "owner_id": new_place.owner.id,
        }, 201

    @api.response(200, "List of places retrieved successfully")
    def get(self) -> tuple:
        """Retrieve full list of places.

        Returns:
            A list of all places.

        """
        places = facade.get_all_places()

        return [
            {
                "id": p.id,
                "title": p.title,
                "latitude": p.latitude,
                "longitude": p.longitude,
            }
            for p in places
        ], 200


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
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": place.owner.id,
                "first_name": place.owner.first_name,
                "last_name": place.owner.last_name,
                "email": place.owner.email,
            }
            if place.owner
            else None,
            "amenities": [
                {
                    "id": facade.get_amenity(a).id,
                    "name": facade.get_amenity(a).name,
                }
                for a in getattr(place, "amenities", [])
            ],
        }, 200

    @api.expect(place_model, validate=True)
    @api.response(200, "Place successfully updated")
    @api.response(404, "Place not found")
    @api.response(400, "Invalid input data")
    def put(self, place_id: str) -> tuple:
        """Update place data.

        Returns:
            Updated data of place.

        """
        place_data = api.payload

        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        updated_place = facade.update_place(place_id, place_data)
        if updated_place is None:
            return {"error": "invalid user"}, 400

        return {
            "id": updated_place.id,
            "title": updated_place.title,
            "description": updated_place.description,
            "price": updated_place.price,
            "latitude": updated_place.latitude,
            "longitude": updated_place.longitude,
        }, 200


# endpoint for reviews


@api.route("/<place_id>/reviews")
class PlaceReviewList(Resource):
    """API endpoint for listing rreviews of a place."""

    def get(self, place_id: str) -> tuple:
        """Get all reviews for a place.

        Returns:
            List of review for given place.

        """
        reviews = facade.get_reviews_by_place(place_id)

        if reviews is None:
            return {"error": "Place not found"}, 404

        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user.id,
            }
            for r in reviews
        ], 200
