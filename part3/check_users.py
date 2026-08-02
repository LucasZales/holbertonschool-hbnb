from app import create_app

app = create_app()

with app.app_context():
    from app.services import facade

    users = facade.get_user_list()

    for user in users:
        print(user.email)
        print(user.password)
        print("----------------")
