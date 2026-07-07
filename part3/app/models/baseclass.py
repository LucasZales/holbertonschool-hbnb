"""Module containing the HBnB BaseModel class."""

# IMPORTS
from app import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    """BaseModel class for HBnB."""

    __abstract__ = True
    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def save(self) -> None:
        """Update modification timestamp."""
        self.updated_at = datetime.now()

    def update(self, data: dict) -> None:
        """Update object attributes.

        Raises:
            TypeError: If data is not a dictionary.

        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
