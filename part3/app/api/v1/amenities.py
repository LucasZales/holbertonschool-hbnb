"""api/v1/amenities api endpoint."""

from app.exception.notfound import NotFoundError
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.api.v1.api_models import amenity_model, amenity_model_place

api = Namespace("amenities", description="Amenity operations")


@api.route("/")
class AmenityList(Resource):
	"""API endpoints for creating and listing ameneities."""

	@jwt_required()
	@api.expect(amenity_model)
	@api.response(201, "Amenity successfully created")
	@api.response(400, "Invalid input data")
	def post(self) -> tuple:
		"""Register a new amenity.

		Returns:
		Data of created amenity.

		"""
		user_id = get_jwt_identity()
		amenity_data = api.payload
		try:
			facade.authorise(True, user_id)
			new_amenity = facade.create_amenity(amenity_data)
		except NotFoundError as e:
			return {"error": str(e)}, 404
		except ValueError as e:
			return {"error": str(e)}, 400
		return api.marshal(new_amenity, amenity_model_place), 201

	@api.response(200, "List of amenities retrieved successfully")
	def get(self) -> tuple:
		"""Retrieve a list of all amenities.

		Returns:
		The full list of amenities.

		"""
		amenities = facade.get_all_amenities()
		return api.marshal(amenities, amenity_model_place), 200


@api.route("/<amenity_id>")
class AmenityResource(Resource):
	"""API endpoints for getting and updating specific amenities."""

	@api.response(200, "Amenity details retrieved successfully")
	@api.response(404, "Amenity not found")
	def get(self, amenity_id: str) -> tuple:
		"""Get amenity details by ID.

		Returns:
			Amenity details, if found.

		"""
		try:
			amenity = facade.get_amenity(amenity_id)
		except NotFoundError as e:
			return {"error": str(e)}, 404
		return api.marshal(amenity, amenity_model_place), 200

	@jwt_required()
	@api.expect(amenity_model)
	@api.response(200, "Amenity updated successfully")
	@api.response(404, "Amenity not found")
	@api.response(400, "Invalid input data")
	def put(self, amenity_id: str) -> tuple:
		"""Update an amenity's information.

		Returns:
			Success or failure message

		"""
		try:
			amenity = facade.get_amenity(amenity_id)
		except NotFoundError as e:
			return {"error": str(e)}, 404
		user_id = get_jwt_identity()

		amenity_data = api.payload
		try:
			facade.authorise(True, user_id, resource)
			facade.update_amenity(amenity_id, amenity_data)
		except NotFoundError as e:
			return {"error": str(e)}, 404
		except ValueError as e:
			return {"error": str(e)}, 400
		return {"message": "Amenity updated successfully"}, 200
