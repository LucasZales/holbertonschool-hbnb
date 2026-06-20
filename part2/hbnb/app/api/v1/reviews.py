"""api/v1/reviews api endpoint."""

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model(
    "Review",
    {
        "text": fields.String(required=True, description="Text of the review"),
        "rating": fields.Integer(required=True, description="Rating (1-5)"),
        "user_id": fields.String(required=True, description="User ID"),
        "place_id": fields.String(required=True, description="Place ID"),
    },
)


@api.route("/")
class ReviewList(Resource):

    @api.expect(review_model, validate=True)
    def post(self):
        """Create a review"""
        data = api.payload

        try:
            review = facade.create_review(data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id,
        }, 201

    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()

        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user.id,
                "place_id": r.place.id,
            }
            for r in reviews
        ], 200


@api.route("/<review_id>")
class ReviewResource(Resource):

    def get(self, review_id):
        """Get review by id"""
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id,
        }, 200

    @api.expect(review_model, validate=True)
    def put(self, review_id):
        """Update review"""
        data = api.payload

        review = facade.update_review(review_id, data)

        if not review:
            return {"error": "Review not found"}, 404

        return {"message": "Review updated successfully"}, 200

    def delete(self, review_id):
        """Delete review"""
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200