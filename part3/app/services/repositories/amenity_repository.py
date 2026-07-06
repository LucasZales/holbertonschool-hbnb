from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self) -> None:
        super().__init__(Amenity)
