```mermaid
sequenceDiagram
actor User
participant PresentationLayer 
participant Logic
participant Database

User->>+PresentationLayer: Place Search Request
PresentationLayer->>+Logic: Place Search Request
Logic->>+Database: Retrive Matches
Database->>-Logic: Matched Places
Logic-->>-PresentationLayer: Matches
PresentationLayer->>-User: Results
```
