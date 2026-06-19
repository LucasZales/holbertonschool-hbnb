"""Module containing the HBnBFacade class."""

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place


class HBnBFacade:
    """Facade layer to handle communication between layers."""

    def __init__(self) -> None:
        """Init for HBnBFacade class."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User methods
    def create_user(self, user_data: dict) -> User:
        """Create a user object and add it to the database.

        Returns:
            The user object.

        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> User | None:
        """Retive User object by id.

        Returns:
            ...

        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email: str) -> User | None:
        """Retive a user object by email.

        Returns:
            User object.

        """
        return self.user_repo.get_by_attribute("email", email)

    def get_user_list(self) -> list:
        """Retrive a list of all users.

        Returns:
            list of all user objects

        """
        return self.user_repo.get_all()

    def update_user(self, user_id: str, user_data: dict) -> User | None:
        """Update a user object.

        Returns:
            updated user object

        """
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id: str):
        # Logic will be implemented in later tasks
        pass

    def create_place(self, place_data):
        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")
        place_data["owner"] = owner
        del place_data["owner_id"]
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    # Amenity methods
    def create_amenity(self, amenity_data: dict) -> Amenity:
        """Create amenity and save to database.

        Returns:
            Created amenity object

        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str) -> Amenity | None:
        """Retrive amenity object by id.

        Returns:
            amenity object or None

        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self) -> list:
        """Retive a list of all amenity objects in the database.

        Returns:
            list of amenity objects

        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id: str, amenity_data: dict) -> None:
        """Update an amenity."""
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
