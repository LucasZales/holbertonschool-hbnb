from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    def __init__(self) -> None:
        super().__init__(Place)
