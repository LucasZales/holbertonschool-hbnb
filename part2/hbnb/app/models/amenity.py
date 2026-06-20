"""Module containing the hbnb amenity class."""

# IMPORTS
import uuid
from datetime import datetime
from app.models.base import Base


class Amenity(Base):
    """Amenity class for hbnb."""

    def __init__(self, name: str) -> None:
        """Init for Amenity class."""
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    # GETTERS AND SETTERS
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("first name must be a string")
        if name == "":
            raise ValueError("Name cannot be empty")
        if len(name) > 50:
            raise ValueError("Name cannot exceed 50 characters")
        self.__name = name
