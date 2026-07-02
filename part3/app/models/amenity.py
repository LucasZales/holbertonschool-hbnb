"""Module containing the HBnB Amenity class."""

# IMPORTS
from app.models.base import Base


class Amenity(Base):
    """Amenity class for HBnB."""

    def __init__(self, name: str) -> None:
        """Init for Amenity class."""
        super().__init__()
        self.name = name

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
