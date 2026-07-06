"""Module containing the HBnB Review class."""

# IMPORTS
from app.models.baseclass import BaseModel
from app import db
from sqlalchemy.orm import validates


class Review(BaseModel):
    """Review class for HBnB."""

    __tablename__ = "reviews"
    text = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.String, db.ForeignKey("places.id"), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)

    def __init__(
        self,
        text: str,
        rating: int,
        user: BaseModel,
        place: BaseModel,
    ) -> None:
        """Init for Review class."""
        super().__init__()
        self.text = text
        self.rating = rating
        self.user_id = user.id
        self.place_id = place.id

    # VALIDATERS
    @validates("text")
    def validate_text(self, _key: str, text: str) -> str:
        """Validate text.

        Returns:
            text if all checks pass

        Raises:
            TypeError: if text is not a string.
            ValueError: if text is empty

        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if not text.strip():
            raise ValueError("text cannot be empty")
        return text

    @validates("rating")
    def validate_rating(self, _key: str, rating: int) -> int:
        """Validate rating.

        Returns:
            rating if all checks pass

        Raises:
            TypeError: if rating is not an int.
            ValueError: if rating is not between 1 and 5

        """
        if not isinstance(rating, int):
            raise TypeError("rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")
        return rating

    @validates("place")
    def validate_place(self, _key: str, place: BaseModel) -> BaseModel:
        """Validate place.

        Returns:
            place if all checks pass

        Raises:
            TypeError: if place is not an instance of the place class.

        """
        if not isinstance(place, BaseModel):
            raise TypeError("place must be a Place instance")
        return place

    @validates("user")
    def validate_user(self, _key: str, user: BaseModel) -> BaseModel:
        """Validate user.

        Returns:
            user if all checks pass

        Raises:
            TypeError: if user is not an instance of user class.

        """
        if not isinstance(user, BaseModel):
            raise TypeError("user must be a User instance")
        return user
