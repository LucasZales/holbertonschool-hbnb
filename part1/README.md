# HBnB Evolution - Technical Documentation

## Task 0 - High-Level Package Diagram
```mermaid
classDiagram
direction TB
    class PresentationLayer {
	    +FacadePattern
	    +ServiceAPI
    }

    class PersistenceLayer {
	    +UserAccess
	    +AmenityAccess
	    +PlaceAccess
	    +ReviewAccess
    }

    class BusinessLogicLayer {
	    +UserClass
	    +AmenityClass
	    +PlaceClass
	    +ReviewClass
    }

    PresentationLayer <--> BusinessLogicLayer : Facade Pattern
    BusinessLogicLayer <--> PersistenceLayer : Database Operations
```
## Layer Descriptions

### Presentation Layer -- BRENDAN --
A simplified GUI designed for user simplified user interaction. This layer will handle user interface, input and communication with the backend services. This layer should display public and relevant data to users, handle page navigation and UI interactions. The presentation layer should include login forms, listings, review submission forms, and filtering interfaces.

### Business Logic Layer -- SEABASS --
The Business Logic Layer is the internal logic of the system handling calls passed to it,
validating requests for data and to save data, and handles all real tasks of the system,
formating data for saving and understanding the systems state from the database.
for instance, when a user tries to sign in the hbnb,
the Presentation Layer will pass the sign in details to the BLL (Business Logic Layer),
and the BLL will request the approate details from the Persistence Layer,
but the BLL will do the aproriate compaisions and confirm success or failuer,
then respond to the Presentation Layer.

### Persistence Layer -- LUCAS --
The Persistence Layer is the part of the application that saves and loads data from the database.In this proyect, it handles storing, updating, deleting, and retrieving information about User, Place, Review, and Amenities.This layer keeps the database logic separate from the rest of the application.

### Facade Pattern
The Facade Pattern is a manager acting as the gatekeeper between the user interface and a complex subsystem which contains lots of moving parts. Imagine a hotel front desk in the real world, where a client presents in an attempt to book a room. The manager at the front desk simplifies the process by understanding the hotel's processes but presenting the information to the client in a way that they understand and does not contain unnecessary additional information. In HBnB, the Facade Pattern sits within the Presentation Layer and acts as the sole communication point between the Presentation Layer and the Business Logic Layer.
