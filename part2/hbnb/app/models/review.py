from app.models.base import Base
from app.models.user import User
from app.models.place import Place


class Review(Base):
    def __init__(self, text, rating, user, place):
        super().__init__()

        if not text:
            raise ValueError("text cannot be empty")

        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")

        self.text = text
        self.rating = rating
        self.user = user
        self.place = place