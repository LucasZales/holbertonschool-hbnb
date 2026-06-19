"""Module containing the hbnb amenity class."""

# IMPORTS
import uuid
from datetime import datetime


class Amenity:
    """Amenity class for hbnb."""

    def __init__(self, name: str) -> None:
        """Init for Amenity class."""
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()

    def update(self, data: dict) -> None:
        """Update the attributes of the object based on the provided dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    # GETTERS AND SETTERS
    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id: str) -> None:
        if not isinstance(id, str):
            raise TypeError("id must be UUIDv4 of type str")
        if len(id) != 36:
            raise TypeError("id must be UUIDv4 of type str")
        self.__id = id

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

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at: datetime) -> None:
        self.__created_at = created_at

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, updated_at: datetime) -> None:
        self.__updated_at = updated_at
