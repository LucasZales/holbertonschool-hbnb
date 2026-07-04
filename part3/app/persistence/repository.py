"""Module containing the InMemoryRepository for HBnB."""

from abc import ABC, abstractmethod
from app.models.base import BaseModel


class Repository[BaseType: BaseModel](ABC):
    """Base class for in memory repository."""

    @abstractmethod
    def add(self, obj: BaseType) -> None:
        pass

    @abstractmethod
    def get(self, obj_id: str) -> BaseType | None:
        pass

    @abstractmethod
    def get_all(self) -> list:
        pass

    @abstractmethod
    def update(self, obj_id: str, data: dict) -> None:
        pass

    @abstractmethod
    def delete(self, obj_id: str) -> None:
        pass

    @abstractmethod
    def get_by_attribute(
        self, attr_name: str, attr_value: object
    ) -> BaseType | None:
        pass


class InMemoryRepository[BaseType: BaseModel](Repository):
    """InMemoryRepository class for HBnB."""

    def __init__(self) -> None:
        """Init for InMemoryRepository."""
        self._storage = {}

    def add(self, obj: BaseType) -> None:
        """Add object to repo under key 'id'."""
        self._storage[obj.id] = obj

    def get(self, obj_id: str) -> BaseType | None:
        """Get and object by its id.

        Returns:
            Object with the given id.

        """
        return self._storage.get(obj_id)

    def get_all(self) -> list:
        """Get all objects in the ropo.

        Returns:
            list of all objects in the repo

        """
        return list(self._storage.values())

    def update(self, obj_id: str, data: dict) -> None:
        """Update and object in the repo."""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id: str) -> None:
        """Delete an object from the repo."""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(
        self, attr_name: str, attr_value: object
    ) -> BaseType | None:
        """Get and object by an antribute.

        Returns:
            Object with the attibute value pair or none

        """
        return next(
            (
                obj
                for obj in self._storage.values()
                if getattr(obj, attr_name) == attr_value
            ),
            None,
        )
