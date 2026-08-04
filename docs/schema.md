```mermaid
erDiagram
    AUTH_USER ||--|| USEPROFILE : extends
    AUTH_USER ||--o{ WORKOUTPLAN : creates
    WORKOUTPLAN ||--o{ WORKOUTLOG : produces
    AUTH_USER ||--o{ CHECKIN : submits
```
