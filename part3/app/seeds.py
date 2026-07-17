from app import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


def seed():

    # USERS
    admin = User.query.filter_by(email="admin@hbnb.com").first()
    if not admin:
        admin = User(
            first_name="Admin",
            last_name="User",
            email="admin@hbnb.com",
            password="admin123",
            is_admin=True
        )
        db.session.add(admin)

    john = User.query.filter_by(email="john@example.com").first()
    if not john:
        john = User(
            first_name="John",
            last_name="Smith",
            email="john@example.com",
            password="password123"
        )
        db.session.add(john)

    jane = User.query.filter_by(email="jane@example.com").first()
    if not jane:
        jane = User(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            password="password123"
        )
        db.session.add(jane)

    # AMENITIES
    wifi = Amenity.query.filter_by(name="WiFi").first()
    if not wifi:
        wifi = Amenity(
            name="WiFi"
        )
        db.session.add(wifi)

    pool = Amenity.query.filter_by(name="Swimming Pool").first()
    if not pool:
        pool = Amenity(
            name="Swimming Pool"
        )
        db.session.add(pool)

    parking = Amenity.query.filter_by(name="Parking").first()
    if not parking:
        parking = Amenity(
            name="Parking"
        )
        db.session.add(parking)

    # PLACES
    beach_house = Place.query.filter_by(title="Beach House").first()
    if not beach_house:
        beach_house = Place(
            title="Beach House",
            description="Beautiful house near the beach",
            price=250.00,
            latitude=-37.8136,
            longitude=144.9631,
            owner=john,
            amenities=[
                wifi,
                parking
            ]
        )
        db.session.add(beach_house)

    city_apartment = Place.query.filter_by(title="City Apartment").first()
    if not city_apartment:
        city_apartment = Place(
            title="City Apartment",
            description="Modern apartment in the city",
            price=180.00,
            latitude=-37.814,
            longitude=144.965,
            owner=jane,
            amenities=[
                wifi,
                pool
            ]
        )
        db.session.add(city_apartment)

    # REVIEWS
    review1 = Review.query.filter_by(place=beach_house).first()
    if not review1:
        review1 = Review(
            text="Amazing place, great location!",
            rating=5,
            user=jane,
            place=beach_house
        )
        db.session.add(review1)

    review2 = Review.query.filter_by(place=city_apartment)
    if not review2:
        review2 = Review(
            text="Very comfortable apartment.",
            rating=4,
            user=john,
            place=city_apartment
        )
        db.session.add(review2)

    db.session.commit()
