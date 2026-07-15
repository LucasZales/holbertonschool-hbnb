"""api/v1/reviews api endpoint."""

from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt_identity
from flask_restx import Namespace, Resource
from app.services import facade
from app.exception.notfound import NotFoundError
from app.api.v1.api_models import (
	review_model_full,
	review_model_creation as review_model,
)

api = Namespace("reviews", description="Review operations")


@api.route("/")
class ReviewList(Resource):
	"""API endpoints for creating and listing reviews."""

	@api.expect(review_model, validate=True)
	@jwt_required()
	def post(self) -> tuple:
		"""Create a review.

		Returns:
			Data of created review.

		"""
		data = api.payload

		jwt_id = get_jwt_identity()
		user_id = data["user_id"]
		place_id = data["place_id"]

		# Remove in future, just here until this is no longer possible
		if jwt_id != user_id:
			return {
				"error": f"user_id and jwt do not match: \nuser_id = {user_id}, \njwt_id =  {jwt_id}"
			}, 400

		if user_id is place.owner_id:
			current_user = get_jwt()
			if not current_user.get('is_admin'):
				return {"error": "Unauthorized action."}, 403

		try:
			place = facade.get_place(place_id)
		except NotFoundError as e:
			return {"error": str(e)}, 404

		if user_id == place.owner_id:
			return {"error": "user cannot review their own place"}, 400

		if user_id in [x for x in place.reviews]:
			return {}, 400

		try:
			review = facade.create_review(data)
		except NotFoundError as e:
			return {"error": str(e)}, 404
		except ValueError as e:
			return {"error": str(e)}, 400

		return api.marshal(review, review_model_full), 201

	def get(self) -> tuple:
		"""Get all reviews.

		Returns:
			List of all reviews

		"""
		reviews = facade.get_all_reviews()

		return api.marshal(
			reviews, review_model_full, mask="{id, text, rating}"
		), 200


@api.route("/<review_id>")
class ReviewResource(Resource):
	"""API endpoints for getting, updating and deleting reviews."""

	def get(self, review_id: str) -> tuple:
		"""Get review by id.

		Returns:
			Data of review with given id.

		"""
		try:
			review = facade.get_review(review_id)
		except NotFoundError as e:
			return {"error": str(e)}, 404

		return api.marshal(review, review_model_full), 200

    @jwt_authorise(facade.get_place)
	@api.expect(review_model)
	def put(self, review) -> tuple:
		"""Update review.

		Returns:
			Data of update review.

		"""
		data = api.payload

		try:
			facade.update_review(review_id, data)
		except NotFoundError as e:
			return {"error": str(e)}, 404

		return {"message": "Review updated successfully"}, 200

    @jwt_authorise(facade.get_place)
	def delete(self, review) -> tuple:
		"""Delete review.

		Returns:
			Success status.

		"""

		try:
			facade.delete_review(review_id)
		except NotFoundError as e:
			return {"error": str(e)}, 404
		return {"message": "Review deleted successfully"}, 200
