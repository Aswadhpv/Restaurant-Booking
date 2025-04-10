# Restaurant Table Booking API

This project is a REST API service for managing restaurant table bookings. It provides endpoints for:
- Managing tables (listing, creating, deleting)
- Managing reservations (listing, creating, deleting)
The project is built using FastAPI, SQLAlchemy (with Alembic for migrations), PostgreSQL, and Docker Compose.

## Features
- REST API built with FastAPI.
- Database management using SQLAlchemy with PostgreSQL.
- Conflict checking: Reservations can only be created if the table is free in the requested time slot.
- Database migrations handled with Alembic.
- Docker & Docker Compose for easy containerized deployment.
- Basic tests with pytest.

- **Tables API:**  
  - `GET /tables/` – Retrieve all tables.
  - `POST /tables/` – Create a new table.
  - `DELETE /tables/{id}` – Delete a specific table.

- **Reservations API:**  
  - `GET /reservations/` – Retrieve all reservations.
  - `POST /reservations/` – Create a new reservation with conflict-checking.
  - `DELETE /reservations/{id}` – Delete a reservation.

- **Database Migrations:**  
  - Manage schema using Alembic.
  
- **Docker Integration:**  
  - Run the application and PostgreSQL using Docker Compose.
  
- **Automated Tests:**  
  - Basic tests using pytest ensuring key functionalities work as expected.

## Project Structure

restaurant_booking/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── routers/
├── tests/
├── alembic/
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
└── requirements.txt


## Setup and Run

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- (Optional) [PyCharm](https://www.jetbrains.com/pycharm/) or any IDE of your choice

### Running the application

1. **Clone the repository** (or open the project folder in PyCharm).
   ```bash
    git clone https://github.com/Aswadhpv/Restaurant-Booking.git
    cd restaurant_booking

2. **Build and start containers:**

   In your project root, run:
   ```bash
   docker-compose up --build
   
3. API --access
  
   ```bash
    API URL: http://localhost:8000
    Swagger UI: http://localhost:8000/docs

4. Database Migrations with Alembic
   
   ```bash
   docker-compose run app alembic upgrade head 


5. Running Tests

   ```bash
   docker-compose run app pytest
If necessary, you can also include the --remove-orphans flag to clean up any orphan containers:
   ```bash   
   docker-compose run --remove-orphans app pytest
   ```

6. Cleaning Up

  ```bash
  docker-compose down --remove-orphans
  ```

## Instructions to correctly execute Program:

1. If Using Pytest:
   
  1. Remove Orphans to not to have conflicts:
   ```bash
  docker-compose down --remove-orphans 
   ```
  2. Update the Migration:
   ```bash
   docker-compose run app alembic upgrade head
   ```
  3. Run the Pytest:
   ```bash
  docker-compose run app pytest 
   ```

2. If you are using Docker after Pytest: (Use this instructions if doing first time or after Pytest or else you can directly go to step 4)
   
  1. Remove Orphans:
  ```bash
  docker-compose down --remove-orphans
  ```
  2. Create a new Migration:
  ```bash
  docker-compose run app alembic revision --autogenerate -m "message"
  ```
  3. Update the Migration:
  ```bash
  docker-compose run app alembic upgrade head
  ```
  4. Run Docker:
  ```bash
  docker-compose up --build 
  ```
