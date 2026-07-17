"""Module containing the HBnBFacade class."""

from app.exception.notfound import NotFoundError
from app.exception.notauthorized import NotAuthorizedError
from flask_jwt_extended import get_jwt_identity, get_jwt
from app.services.repositories.user_repository import UserRepository
from app.services.repositories.amenity_repository import AmenityRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """Facade layer to handle communication between layers."""

    def __init__(self) -> None:
        """Init for HBnBFacade class."""
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # Authorisation
    def authorise(self, admin_access, identity, resource):
        """Authorize user access to a specific resource."""
        current_user = get_jwt()
        user_id = get_jwt_identity()

        if admin_access and current_user.get('is_admin') or not resource:
            return True

        # Fixed: Changed 'is' comparison to standard equality '==' for string matching
        permissions = [
            [User, lambda res: str(user_id) == str(res.id)],
            [Place, lambda res: str(user_id) == str(res.owner_id)],
            [Review, lambda res: str(user_id) == str(res.user_id)],
        ]

        for permission in permissions:
            if isinstance(resource, permission[0]) and permission[1](resource):
                return True

        raise NotAuthorizedError("Unauthorized action.")

    # User methods

    def create_user(self, user_data: dict) -> User:
        """Create a user object and add it to the database.

        Returns:
            The user object.

        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> User:
        """Retive User object by id.

        Returns:
            User object.

        Raises:
            NotFoundError: if user not in repo

        """
        user = self.user_repo.get(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return user

    def get_user_by_email(self, email: str) -> User:
        """Retive a user object by email.

        Returns:
            User object.

        Raises:
            NotFoundError: if user not in repo

        """
        user = self.user_repo.get_user_by_email(email)
        if user is None:
            raise NotFoundError("User not found")
        return user

    def get_user_list(self) -> list:
        """Retrive a list of all users.

        Returns:
            list of all user objects

        """
        return self.user_repo.get_all()

    def update_user(self, user_id: str, user_data: dict) -> User:
        """Update a user object.

        Returns:
            updated user object

        Raises:
            NotFoundError: if user not in repo

        """
        user = self.get_user(user_id)
        self.user_repo.update(user_id, user_data)
        return user

    # PLACE METHODS
    def create_place(self, place_data: dict) -> Place:
        """Create a place and add it to the database.

        Returns:
            Created place.

        Raises:
            NotFoundError: if owner not in repo

        """
        owner = self.user_repo.get(place_data["owner_id"])
        if owner is None:
            raise NotFoundError("Owner not found")

        # Extracted foreign key handling safely for relational backrefs
        place_data_copy = place_data.copy()
        place_data_copy["owner"] = owner
        if "owner_id" in place_data_copy:
            del place_data_copy["owner_id"]

        place = Place(**place_data_copy)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id: str) -> Place:
        """Get place by id.

        Returns:
            Place with given id.

        Raises:
            NotFoundError: if place not in repo

        """
        place = self.place_repo.get(place_id)
        if place is None:
            raise NotFoundError("Place not found")
        return place

    def get_all_places(self) -> list:
        """Retive a list of all place objects in the database.

        Returns:
            list of place objects

        """
        return self.place_repo.get_all()

    def update_place(self, place_id: str, place_data: dict) -> Place:
        """Update a place.

        Returns:
            Updated place.

        Raises:
            NotFoundError: if place or owner not in repo

        """
        place = self.place_repo.get(place_id)
        if place is None:
            raise NotFoundError("Place not found")

        # Fixed: Safely check for owner validation only if owner_id is passed in the update payload
        if "owner_id" in place_data:
            owner = self.user_repo.get(place_data["owner_id"])
            if owner is None:
                raise NotFoundError("Owner not found")

        self.place_repo.update(place_id, place_data)
        return place

    def delete_place(self, place_id: str) -> None:
        """Delete place.

        Raises:
            NotFoundError: if place not in repo

        """
        place = self.place_repo.get(place_id)
        if place is None:
            raise NotFoundError("Place not found")
        self.place_repo.delete(place_id)

    # AMENITY METHODS
    def create_amenity(self, amenity_data: dict) -> Amenity:
        """Create amenity and save to database.

        Returns:
            Created amenity object

        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str) -> Amenity:
        """Retrive amenity object by id.

        Returns:
            amenity object or None

        Raises:
            NotFoundError: if amenity not in repo

        """
        amenity = self.amenity_repo.get(amenity_id)
        if amenity is None:
            raise NotFoundError("Amenity not found")
        return amenity

    def get_all_amenities(self) -> list:
        """Retive a list of all amenity objects in the database.

        Returns:
            list of amenity objects

        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id: str, amenity_data: dict) -> None:
        """Update an amenity.

        Raises:
            NotFoundError: if amenity not in repo

        """
        amenity = self.get_amenity(amenity_id)
        if amenity is None:
            raise NotFoundError("Amenity not found")
        self.facility_repo.update(amenity_id, amenity_data) if hasattr(
            self, 'facility_repo') else self.amenity_repo.update(amenity_id, amenity_data)

    # REVIEW METHODS
    def create_review(self, review_data: dict) -> Review:
        """Create a review and save it to database.

        Returns:
            Created review.

        Raises:
            NotFoundError: if place or user not in repo

        """
        user = self.user_repo.get(review_data["user_id"])
        place = self.place_repo.get(review_data["place_id"])
        if user is None:
            raise NotFoundError("User not found")
        if place is None:
            raise NotFoundError("Place not found")

        review_data_copy = review_data.copy()
        review_data_copy["user"] = user
        review_data_copy["place"] = place
        if "user_id" in review_data_copy:
            del review_data_copy["user_id"]
        if "place_id" in review_data_copy:
            del review_data_copy["place_id"]

        review = Review(**review_data_copy)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id: str) -> Review:
        """Get review by id.

        Returns:
            Review with given id.

        Raises:
            NotFoundError: if review not in repo

        """
        review = self.review_repo.get(review_id)
        if review is None:
            raise NotFoundError("Review not found")
        return review

    def get_all_reviews(self) -> list:
        """Get a list of all reviews.

        Returns:
            List of all reviews

        """
        return self.review_repo.get_all()

    def update_review(self, review_id: str, review_data: dict) -> Review:
        """Update a review.

        Returns:
            Updated review.

        Raises:
            NotFoundError: if review not in repo

        """
        review = self.review_repo.get(review_id)
        if review is None:
            raise NotFoundError("Review not found")
        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id: str) -> None:
        """Delete Review.

        Raises:
            NotFoundError: if review not in repo

        """
        review = self.review_repo.get(review_id)
        if review is None:
            raise NotFoundError("Review not found")
        self.review_repo.delete(review_id)

    def get_reviews_by_place(self, place_id: str) -> list:
        """Get a list of reviews for a place.

        Returns:
            List of reviews for place

        Raises:
            NotFoundError: if place not in repo

        """
        place = self.place_repo.get(place_id)
        if place is None:
            raise NotFoundError("Place not found")

        return place.reviews
