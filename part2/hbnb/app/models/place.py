"""Module containing the HBnB Place class."""

# IMPORTS
from app.models.base import Base


class Place(Base):
    """Place class for HBnB."""

    def __init__(
        self,
        title: str,
        price: float,
        latitude: float,
        longitude: float,
        owner: Base,
        description: str = "",
        amenities: list | None = None,
    ) -> None:
        """Init for Place class."""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = amenities if amenities is not None else []

    def add_review(self, review: Base) -> None:
        """Add review to place."""
        self.reviews.append(review)

    def add_amenity(self, amenity: Base) -> None:
        """Add amenity to place."""
        self.amenities.append(amenity)

    @property
    def amenities(self) -> list:
        return self.__amenities

    @amenities.setter
    def amenities(self, value: list) -> None:
        if not isinstance(value, list):
            raise TypeError("Amenities must be a list")
        self.__amenities = value

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str) -> None:
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if not title.strip():
            raise ValueError("title cannot be empty")
        if len(title) > 100:
            raise ValueError("title must be 100 characters or less")
        self.__title = title

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        self.__description = description

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, price: float) -> None:
        if not isinstance(price, (int, float)):
            raise TypeError("price must be a number")
        if price <= 0:
            raise ValueError("price must be greater than zero")
        self.__price = float(price)

    @property
    def latitude(self) -> float:
        return self.__latitude

    @latitude.setter
    def latitude(self, latitude: float) -> None:
        if not isinstance(latitude, (int, float)):
            raise TypeError("latitude must be a number")
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("latitude must be between -90.0 and 90.0")
        self.__latitude = float(latitude)

    @property
    def longitude(self) -> float:
        return self.__longitude

    @longitude.setter
    def longitude(self, longitude: float) -> None:
        if not isinstance(longitude, (int, float)):
            raise TypeError("longitude must be a number")
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("longitude must be between -180.0 and 180.0")
        self.__longitude = float(longitude)

    @property
    def owner(self) -> Base:
        return self.__owner

    @owner.setter
    def owner(self, owner: Base) -> None:
        if not isinstance(owner, Base):
            raise TypeError("owner must be a User instance")
        self.__owner = owner
