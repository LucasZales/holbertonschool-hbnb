from app import db
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self) -> None:
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def update(self, user_id, data):
        user = self.get(user_id)

        print("BEFORE:", user.password)
        print("DATA:", data)

        if user is None:
            raise NotFoundError("User not found.")

        if "email" in data:
            existing_user = self.get_user_by_email(data["email"])
            if existing_user and existing_user.id != user.id:
                raise ValueError("Email already registered.")

        for key, value in data.items():
            print("SETTING:", key, value)
            if hasattr(user, key):
                setattr(user, key, value)

        db.session.commit()

        print("AFTER:", user.password)

        return user
