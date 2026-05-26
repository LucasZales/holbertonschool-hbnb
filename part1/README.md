# HBnB Evolution - Technical Documentation

## High-Level Package Diagram

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
    
## Layer Descriptions

### Presentation Layer -- BRENDAN --

### Business Logic Layer -- SEABASS --

### Persistence Layer -- LUCAS --

### Facade Pattern
