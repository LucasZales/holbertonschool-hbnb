"""Module containing the HBnBFacade class."""

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """Facade layer to handle communication between layers."""

    def __init__(self) -> None:
        """Init for HBnBFacade class."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User methods
    def create_user(self, user_data: dict) -> User:
        """Create a user object and add it to the database.

        Returns:
            The user object.

        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> User | None:
        """Retive User object by id.

        Returns:
            User object.

        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email: str) -> User | None:
        """Retive a user object by email.

        Returns:
            User object.

        """
        return self.user_repo.get_by_attribute("email", email)

    def get_user_list(self) -> list:
        """Retrive a list of all users.

        Returns:
            list of all user objects

        """
        return self.user_repo.get_all()

    def update_user(self, user_id: str, user_data: dict) -> User | None:
        """Update a user object.

        Returns:
            updated user object

        """
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)

    # PLACE METHODS
    def create_place(self, place_data: dict) -> Place:
        """Create a place and add it to the database.

        Returns:
            Created place.

        """
        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")
        place_data["owner"] = owner
        del place_data["owner_id"]
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id: str) -> Place | None:
        """Get place by id.

        Returns:
            Place with given id.

        """
        return self.place_repo.get(place_id)

    def get_all_places(self) -> list:
        return self.place_repo.get_all()

    def update_place(self, place_id: str, place_data: dict) -> Place | None:
        self.place_repo.update(place_id, place_data)
        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            return None
        return self.place_repo.get(place_id)

    # AMENITY METHODS
    def create_amenity(self, amenity_data: dict) -> Amenity:
        """Create amenity and save to database.

        Returns:
            Created amenity object

        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str) -> Amenity | None:
        """Retrive amenity object by id.

        Returns:
            amenity object or None

        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self) -> list:
        """Retive a list of all amenity objects in the database.

        Returns:
            list of amenity objects

        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id: str, amenity_data: dict) -> None:
        """Update an amenity."""
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)

    # Review methods
    def create_review(self, review_data: dict) -> Review:
        """Create a review and save it to database.

        Returns:
            Created review.

        """
        user = self.user_repo.get(review_data["user_id"])
        place = self.place_repo.get(review_data["place_id"])

        if not user or not place:
            raise ValueError("User or Place not found")

        if not review_data["text"].strip():
            raise ValueError("Text cannot be empty")

        if review_data["rating"] < 1 or review_data["rating"] > 5:
            raise ValueError("Rating must be between 1 and 5")

        review = Review(
            review_data["text"], review_data["rating"], user, place
        )

        self.review_repo.add(review)
        place.add_review(review)

        return review

    def get_review(self, review_id: str) -> Review | None:
        """Get review by id.

        Returns:
            Review with given id.

        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self) -> list:
        """Get a list of all reviews.

        Returns:
            List of all reviews

        """
        return self.review_repo.get_all()

    def update_review(
        self, review_id: str, review_data: dict
    ) -> Review | None:
        """Update a review.

        Returns:
            Updated review.

        """
        review = self.review_repo.get(review_id)

        if not review:
            return None

        if "text" in review_data:
            review.text = review_data["text"]

        if "rating" in review_data:
            review.rating = review_data["rating"]

        review.save()
        return review

    def delete_review(self, review_id: str) -> None:
        """Delete Review."""
        review = self.review_repo.get(review_id)

        if review:
            if review in review.place.reviews:
                review.place.reviews.remove(review)

        self.review_repo.delete(review_id)

    def get_reviews_by_place(self, place_id: str) -> list:
        """Get a list of reviews for a place.

        Returns:
            List of reviews for place

        """
        place = self.place_repo.get(place_id)

        if not place:
            return []

        return place.reviews
