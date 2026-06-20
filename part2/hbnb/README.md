Document the Project Setup

In the README.md file, write a brief overview of the project setup:

    Describe the purpose of each directory and file.
    Include instructions on how to install dependencies and run the application.



Linux Virtual Environment:
1. In holbertonschool-hbnb/part2/hbnb/ initialise a virtual environment with
python -m venv venv

2. Activate the environment with
source venv/bin/activate

3. Upgrade pip
pip install --upgrade pip

4. Install requirements
pip install -r requirements.txt

5. Run the app with
python run.py

6. Testing:
curl -X POST http://127.0.0.1:5000/api/v1/users/   -H "Content-Type: application/json"   -d '{"first_name": "John", "last_name": "Doe", "email": "test123@testemail.server.com"}'
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ -H "Content-Type: application/json" -d '{"name": "Toilet"}'
curl -X POST http://127.0.0.1:5000/api/v1/places/ -H "Content-Type: application/json" -d '{"title": "Mi Casa", "description": "es su casa", "price": 100, "latitude": 50, "longitude": 80, "owner_id": "{owner_id}", "amenities": []}'

- curl -X POST http://127.0.0.1:5000/api/v1/reviews/ -H "Content-Type: application/json" -d '{"text": "excellent view", "rating": 4, "user_id": "user_id", "place_id": "place_id"}'
