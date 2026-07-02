"""Module containing the HBnB Review class."""

# IMPORTS
from app.models.base import Base


class Review(Base):
    """Review class for HBnB."""

    def __init__(
        self, text: str, rating: int, user: Base, place: Base
    ) -> None:
        """Init for Review class."""
        super().__init__()
        self.text = text
        self.rating = rating
        self.user = user
        self.place = place

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str) -> None:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if not text.strip():
            raise ValueError("text cannot be empty")
        self.__text = text

    @property
    def rating(self) -> int:
        return self.__rating

    @rating.setter
    def rating(self, rating: int) -> None:
        if not isinstance(rating, int):
            raise TypeError("rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")
        self.__rating = rating

    @property
    def user(self) -> Base:
        return self.__user

    @user.setter
    def user(self, user: Base) -> None:
        if not isinstance(user, Base):
            raise TypeError("user must be a User instance")
        self.__user = user

    @property
    def place(self) -> Base:
        return self.__place

    @place.setter
    def place(self, place: Base) -> None:
        if not isinstance(place, Base):
            raise TypeError("place must be a Place instance")
        self.__place = place
