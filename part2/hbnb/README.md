# HBnB – Part 2

## Project Description

This project implements the business logic and REST API for a simplified Airbnb-like application (HBnB). It provides endpoints to manage users, places, reviews, and amenities using a layered architecture with Flask and Flask-RESTX.

Persistence is handled using an in-memory repository.

---

## Project Structure

- `app/api/` – REST API endpoints (Flask-RESTX namespaces)
- `app/models/` – Business entities (User, Place, Review, Amenity)
- `app/services/` – Business logic layer (Facade pattern)
- `app/persistence/` – In-memory storage implementation
- `app/helpers/` – Utility functions (e.g., email validation)
- `config.py` – Application configuration
- `run.py` – Entry point to start the server

---

## Architecture

The application follows a layered architecture:

- **Presentation Layer:** Flask-RESTX API (`app/api`)
- **Business Logic Layer:** Models and Facade (`app/services/facade.py`)
- **Persistence Layer:** In-memory repository (`app/persistence`)

The Facade pattern is used to centralize communication between layers.

---

## Setup Instructions

### 0. Prerequisite
This project uses python3.13 or greater
please ensure that is your version before continuing
```
  python3 -V
```

### 1. Download the Repo
```
  git clone https://github.com/LucasZales/holbertonschool-hbnb.git
```
### 2. Create virtual environment

#### Linux / macOS
```bash
cd holbertonschool-hbnb/part2/hbnb
python3 -m venv venv
```

#### Windows (PowerShell)
```powershell
cd holbertonschool-hbnb\part2\hbnb
python -m venv venv
```

---

### 3. Activate virtual environment

#### Linux / macOS
```bash
source venv/bin/activate
```

#### Windows (PowerShell)
```powershell
venv\Scripts\Activate.ps1
```

---

### 4. Upgrade pip

```bash
pip install --upgrade pip
```

---

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 6. Run the application

```bash
python run.py
```

The API will be available at:

```bash
http://127.0.0.1:5000/api/v1/
```

---

## Testing the API (curl examples)

### Create a user

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{"first_name": "John", "last_name": "Doe", "email": "test123@testemail.server.com"}'
```

---

### Create an amenity

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
-H "Content-Type: application/json" \
-d '{"name": "Toilet"}'
```

---

### Create a place

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{"title": "Mi Casa", "description": "es su casa", "price": 100, "latitude": 50, "longitude": 80, "owner_id": <owner_id>, "amenities": []}'
```

---

### Create a review

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{"text": "excellent view", "rating": 4, "user_id": <user_id>, "place_id": <place_id>}'
```

---

None:
  where <user_id>, <place_id>, ect is used this must be replaced with and apropriate id

## Requirements

- Python 3.13
- Flask
- Flask-RESTX

---

## Notes

- Uses in-memory persistence (no database)
- Input validation handled in models and services
- Facade pattern used to decouple API and business logic
```
