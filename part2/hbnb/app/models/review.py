from app.models.base import Base


class Review(Base):
    def __init__(self, text, rating, user, place):
        super().__init__()

        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if not text.strip():
            raise ValueError("text cannot be empty")

        if not isinstance(rating, int):
            raise TypeError("rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")

        if not isinstance(user, Base):
            raise TypeError("user must be a User instance")

        if not isinstance(place, Base):
            raise TypeError("place must be a Place instance")

        self.text = text
        self.rating = rating
        self.user = user
        self.place = place
