from app.models.base import Base

class Amenity(Base):
    def __init__(self, name):
        super().__init__()
        if not name:
            raise ValueError("Name cannot be empty")
        if len(name) > 50:
            raise ValueError("Name cannot exceed 50 characters")
        self.name = name
