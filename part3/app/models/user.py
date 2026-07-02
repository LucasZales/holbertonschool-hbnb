"""Module containing the HBnB User class."""

# IMPORTS
from app.helpers.email_validator import validate_email
from app.models.base import Base
from app import bcrypt


class User(Base):
    """User class for HBnB."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        is_admin: bool = False,
    ) -> None:
        """Init for User class."""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)
        self.is_admin = is_admin
        self.__places = []

    def add_place(self, place: Base) -> None:
        """Add place to Places list.

        Raises:
            TypeError: if place is not an instance of Place class.

        """
        if not isinstance(place, Base):
            raise TypeError("place must be an instance of Place class.")
        self.__places.append(place)

    def remove_place(self, place_id: str) -> None:
        """Remove place from places list.

        Raises:
            TypeError: if place id is not a string.
            ValueError: if place not found in list.

        """
        if not isinstance(place_id, str):
            raise TypeError("place_id must be a str.")
        place = next(x for x in self.__places if x.id == place_id)
        if not place:
            raise ValueError("Place not found.")
        self.__places.remove(place)

    def hash_password(self, password: str) -> None:
        """Hashes the password before storing it.

        Raises:
            ValueError: if password is an empty string.

        """
        if not password:
            raise ValueError("Password cannot be empty.")
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password: str) -> bool:
        """Verify if the provided password matches the hashed password.

        Returns:
            True if hash of password matches stored hash

        """
        return bcrypt.check_password_hash(self.password, password)

    # GETTERS AND SETTERS
    @property
    def first_name(self) -> str:
        """First name of user."""
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
        """Last name of user."""
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
        """Email of user."""
        return self.__email

    @email.setter
    def email(self, email: str) -> None:
        if not isinstance(email, str):
            raise TypeError("email must be a string")
        if not email.strip():
            raise TypeError("email must not be empty")
        if not validate_email(email):
            raise ValueError("email must be valid")
        self.__email = email

    @property
    def is_admin(self) -> bool:
        """Admin status of user."""
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, is_admin: bool) -> None:
        if not isinstance(is_admin, bool):
            raise TypeError("is_admin must be bool")
        self.__is_admin = is_admin
