"""Module containing the HBnB Amenity class."""

# IMPORTS
from app.models.baseclass import BaseModel
from app import db
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    """Amenity class for HBnB."""

    __tablename__ = "amenities"
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name: str) -> None:
        """Init for Amenity class."""
        super().__init__()
        self.name = name

    # VALIDATERS
    @validates("name")
    def validate_name(self, _key: str, name: str) -> str:
        """Validate amenity name.

        Returns:
            name if all checks pass

        Raises:
            TypeError: if name is not a string
            ValueError: name is empty or over 50 characters

        """
        if not isinstance(name, str):
            raise TypeError("first name must be a string")
        if name == "":
            raise ValueError("Name cannot be empty")
        if len(name) > 50:
            raise ValueError("Name cannot exceed 50 characters")
        return name
