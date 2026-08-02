from app import create_app

app = create_app()

with app.app_context():
    from app.services import facade

    user = facade.get_user_by_email("john.doe@example.com")

    passwords = [
        "upassone",
        "password!",
        "password123",
        "tests@test",
        "upasstwo",
        "pass",
    ]

    print("Usuario:", user.email)

    for password in passwords:
        print(password, "->", user.verify_password(password))
