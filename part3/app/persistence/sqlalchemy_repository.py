"""Module containing the SQLAlchemyRepository."""

from app import db
from app.persistence.repository import Repository
from app.models.base import Base


class SQLAlchemyRepository[BaseType: Base](Repository[BaseType]):
    """Repository implementation using SQLAlchemy."""

    def __init__(self, model):
        self.model = model

    def add(self, obj):
        """Add an object to the database."""
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """Retrieve an object by its ID."""
        return self.model.query.get(obj_id)
    
    def get_all(self):
        """Retrieve all objects."""
        return self.model.query.all()
    
    def update(self, obj_id, data):
        """Update an object."""
        obj = self.get(obj_id)

        if obj:
            for key, value in data.items():
                setattr(obj, key, value)

            db.session.commit()

    def delete(self, obj_id):
        """Delete an object."""
        obj = self.get(obj_id)

        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by one of its attributes."""
        return self.model.query.filter_by(
            **{attr_name: attr_value}
        ).first()