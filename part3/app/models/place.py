"""Module containing the HBnB Place class."""

# IMPORTS
from sqlalchemy.orm import validates
from app.models.baseclass import BaseModel
from app.models.user import User
from app.models.association_tables import place_amenity

# needed for amenites relationship don't remove, will break, probably, im tired
from app.models.amenity import Amenity
from app import db


class Place(BaseModel):
    """Place class for HBnB."""

    __tablename__ = "places"
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    reviews = db.relationship("Review", backref="place", lazy=True)
    owner_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        lazy="subquery",
        backref=db.backref("places", lazy=True),
    )

    def __init__(
        self,
        title: str,
        price: float,
        latitude: float,
        longitude: float,
        owner: User,
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

    def add_review(self, review: BaseModel) -> None:
        """Add review to place."""
        self.reviews.append(review)

    def add_amenity(self, amenity: BaseModel) -> None:
        """Add amenity to place."""
        self.amenities.append(amenity)

    @validates("amenities")
    def validate_amenities(self, _key: str, amenities: list) -> list:
        """Validate amenities list.

        Returns:
            amenities list if all checks pass

        Raises:
            TypeError: if amenities is not a list.

        """
        if not isinstance(amenities, list):
            raise TypeError("Amenities must be a list")
        return amenities

    @validates("title")
    def validate_title(self, _key: str, title: str) -> str:
        """Validate title.

        Returns:
            title if all checks pass

        Raises:
            TypeError: if title is not a string.
            ValueError: if title is empty or over 100 characters.

        """
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if not title.strip():
            raise ValueError("title cannot be empty")
        if len(title) > 100:
            raise ValueError("title must be 100 characters or less")
        return title

    @validates("description")
    def validate_description(self, _key: str, description: str) -> str:
        """Validate description.

        Returns:
            description if all checks pass

        Raises:
            TypeError: if description is not a string.

        """
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        return description

    @validates("price")
    def validate_price(self, _key: str, price: float) -> float:
        """Validate price.

        Returns:
            price if all checks pass

        Raises:
            TypeError: if price is not an int or float.
            ValueError: if price is not above 0.

        """
        if not isinstance(price, (int, float)):
            raise TypeError("price must be a number")
        if price <= 0:
            raise ValueError("price must be greater than zero")
        return price

    @validates("latitude")
    def validate_latitude(self, _key: str, latitude: float) -> float:
        """Validate latitude.

        Returns:
            latitude if all checks pass

        Raises:
            TypeError: if latitude is not an int or float.
            ValueError: if latitude is not between -90.0 and 90.0.

        """
        if not isinstance(latitude, (int, float)):
            raise TypeError("latitude must be a number")
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("latitude must be between -90.0 and 90.0")
        return float(latitude)

    @validates("longitude")
    def validate_longitude(self, _key: str, longitude: float) -> float:
        """Validate longitude.

        Returns:
            longitude if all checks pass

        Raises:
            TypeError: if longitude is not an int or float.
            ValueError: if longitude is not between -180.0 and 180.0.

        """
        if not isinstance(longitude, (int, float)):
            raise TypeError("longitude must be a number")
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("longitude must be between -180.0 and 180.0")
        return float(longitude)

    @validates("owner")
    def validate_owner(self, _key: str, owner: User) -> User:
        """Validate owner.

        Returns:
            owner if all checks pass

        Raises:
            TypeError: if owner is not an instance of User class.

        """
        if not isinstance(owner, User):
            raise TypeError("owner must be a User instance")
        return owner
