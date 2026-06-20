"""api/v1/amenities api endpoint."""

from flask_restx import Namespace, Resource
from app.services import facade
from app.api.v1.api_models import amenity_model

api = Namespace("amenities", description="Amenity operations")


@api.route("/")
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new amenity.

        Returns:
        Data of created amenity.

        """
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {"error": str(e)}, 400
        return {"id": new_amenity.id, "name": new_amenity.name}, 201

    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        """Retrieve a list of all amenities.

        Returns:
        The full list of amenities.

        """
        amenities = facade.get_all_amenities()
        result = []
        for a in amenities:
            result.append({"id": a.id, "name": a.name})
        return result, 200


@api.route("/<amenity_id>")
class AmenityResource(Resource):
    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Get amenity details by ID.

        Return:
        Amenity details, if found.

        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return {"id": amenity.id, "name": amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, "Amenity updated successfully")
    @api.response(404, "Amenity not found")
    @api.response(400, "Invalid input data")
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        try:
            facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            return {"error": str(e)}, 400
        return {"message": "Amenity updated successfully"}, 200
