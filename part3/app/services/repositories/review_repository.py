from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self) -> None:
        super().__init__(Review)
