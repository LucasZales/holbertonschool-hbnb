"""Module containing hbnb User class."""

# IMPORTS
import uuid
from datetime import datetime
from app.helpers.email_validator import validate_email


class User:
    """User class for hbnb."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        is_admin: bool = False,
    ) -> None:
        """Init for User class."""
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
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
    def first_name(self) -> str:
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name: str) -> None:
        if not isinstance(first_name, str):
            raise TypeError("first name must be a string")
        if first_name == "":
            raise ValueError("first name cannot be empty")
        if len(first_name) > 50:
            raise ValueError("first name must be no longer then 50 characters")
        self.__first_name = first_name

    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name: str) -> None:
        if not isinstance(last_name, str):
            raise TypeError("last name must be a string")
        if last_name == "":
            raise ValueError("last name cannot be empty")
        if len(last_name) > 50:
            raise ValueError("last name must be no longer then 50 characters")
        self.__last_name = last_name

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str) -> None:
        if not isinstance(email, str):
            raise TypeError("email must be a string")
        if not validate_email(email):
            raise ValueError("email must be valid")
        self.__email = email

    @property
    def is_admin(self) -> bool:
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, is_admin: bool) -> None:
        if not isinstance(is_admin, bool):
            raise TypeError("is_admin must be bool")
        self.__is_admin = is_admin

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
