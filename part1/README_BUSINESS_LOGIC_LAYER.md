# HBnB proyect - Technical Documentation

## Task 1 - Detailed Class Diagram for Business Logic Layer
```mermaid
classDiagram

class User {
    id
    user_name
    user_lastname
    email
}

class Place {
    id
    title
    price
    dimensions
}

class Review {
    id
    text
    rating
}

class Amenity {
    id
    name
}

User --> Place : owns
User --> Review : writes
Place --> Review : has
Place --> Amenity : includes
```