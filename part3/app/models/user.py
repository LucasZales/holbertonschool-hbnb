"""Module containing the HBnB User class."""

# IMPORTS
from app.helpers.email_validator import validate_email
from app.models.baseclass import BaseModel
from app import bcrypt, db
from sqlalchemy.orm import validates


class User(BaseModel):
    """User class for HBnB."""

    __tablename__ = "users"
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship("Place", backref="owner",
                             lazy=True, cascade="all, delete-orphan",
                             single_parent=True, passive_deletes=True)
    reviews = db.relationship("Review", backref="user",
                              lazy=True, cascade="all, delete-orphan",
                              single_parent=True, passive_deletes=True)

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
        self.password = password
        self.is_admin = is_admin
        # Fixed: Diverted the internal in-memory array list placeholder back to the active dynamic ORM collection mapping proxy
        self.__places = self.places

    def add_place(self, place: BaseModel) -> None:
        """Add place to Places list.

        Raises:
            TypeError: if place is not an instance of Place class.

        """
        if not isinstance(place, BaseModel):
            raise TypeError("place must be an instance of Place class.")
        self.places.append(place)

    def remove_place(self, place_id: str) -> None:
        """Remove place from places list.

        Raises:
            TypeError: if place id is not a string.
            ValueError: if place not found in list.

        """
        if not isinstance(place_id, str):
            raise TypeError("place_id must be a str.")
        try:
            place = next(x for x in self.places if x.id == place_id)
        except StopIteration:
            raise ValueError("Place not found.")
        self.places.remove(place)

    def hash_password(self, password: str) -> None:
        """Hashes the password before storing it.

        Raises:
            ValueError: if password is an empty string.

        """
        if not password:
            raise ValueError("Password cannot be empty.")
        self.password = password

    @validates("password")
    def validate_password(self, _key: str, password: str) -> str:
        """Validate password.

        Returns:
            password if all checks pass

        Raises:
            TypeError: if password is not a string.
            ValueError: if password is empty

        """
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        if not password.strip():
            raise ValueError("Password cannot be empty.")
        if password.startswith('$2b$') or password.startswith('$2a$'):
            return password
        return bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password: str) -> bool:
        """Verify if the provided password matches the hashed password.

        Returns:
            True if hash of password matches stored hash

        """
        return bcrypt.check_password_hash(self.password, password)

    # VALIDATERS
    @validates("first_name")
    def validate_first_name(self, _key: str, first_name: str) -> str:
        """Validate first_name.

        Returns:
            first_name if all checks pass

        Raises:
            TypeError: if first_name is not a string.
            ValueError: if first_name is empty

        """
        if not isinstance(first_name, str):
            raise TypeError("first name must be a string")
        if first_name == "":
            raise ValueError("first name cannot be empty")
        if len(first_name) > 50:
            raise ValueError("first name must be no longer then 50 characters")
        return first_name

    @validates("last_name")
    def validate_last_name(self, _key: str, last_name: str) -> str:
        """Validate last_name.

        Returns:
            last_name if all checks pass

        Raises:
            TypeError: if last_name is not a string.
            ValueError: if last_name is empty

        """
        if not isinstance(last_name, str):
            raise TypeError("last name must be a string")
        if last_name == "":
            raise ValueError("last name cannot be empty")
        if len(last_name) > 50:
            raise ValueError("last name must be no longer then 50 characters")
        return last_name

    @validates("email")
    def validate_email(self, _key: str, email: str) -> str:
        """Validate email.

        Returns:
            email if all checks pass

        Raises:
            TypeError: if email is not a string.
            ValueError: if email is empty

        """
        if not isinstance(email, str):
            raise TypeError("email must be a string")
        # Fixed: Changed ValueError runtime check to match structural signature exception logic matching standard type parameters
        if not email.strip():
            raise ValueError("email must not be empty")
        if not validate_email(email):
            raise ValueError("email must be valid")
        return email

    @validates("is_admin")
    def validate_is_admin(self, _key: str, is_admin: bool) -> bool:
        """Validate is_admin.

        Returns:
            is_admin if all checks pass

        Raises:
            TypeError: if is_admin is not a bool.

        """
        if not isinstance(is_admin, bool):
            raise TypeError("is_admin must be bool")
        return is_admin
