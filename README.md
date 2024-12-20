# Spy Cat Agency Management System

## Overview

The Spy Cat Agency (SCA) Management System is a Django-based CRUD application
designed to manage spy cats, their missions, and associated targets. This
application demonstrates the ability to build RESTful APIs, interact with a
relational database, and integrate third-party services. The application is
structured to handle SCA's specific needs for efficiently assigning and
managing spying tasks.

## Features

### Spy Cats Management

- Create spy cat profiles with fields like **Name**, **Years of Experience**, *
  *Breed**, and **Salary**.
- Update specific attributes of a spy cat, such as their **Salary**.
- Retrieve details of all spy cats or a single cat.
- Remove spy cats from the system.

### Missions Management

- Create missions and assign spy cats to them, along with associated targets.
- Update mission targets:
    - Add or modify notes.
    - Mark targets as complete (frozen notes once complete).
- Assign available cats to missions.
- List all missions or retrieve details of a specific mission.
- Prevent deletion of missions already assigned to cats.

### Targets Management

- Manage mission-specific targets with attributes like **Name**, **Country**, *
  *Notes**, and **Completion Status**.
- Ensure targets cannot be updated once marked as complete.

### Validations

- Validate cat breeds using
  the [TheCatAPI](https://api.thecatapi.com/v1/breeds).
- Ensure appropriate status codes for invalid requests.

---

## Tech Stack

- **Framework**: Django REST Framework
- **Database**: PostgreSQL
- **Third-Party API**: [TheCatAPI](https://api.thecatapi.com/v1/breeds) for
  breed validation

---

## Project Setup

### Prerequisites

- Python 3.12
- A virtual environment (e.g., `venv` or `pipenv`)
- [Postman](https://www.postman.com/downloads/) (optional, for testing API
  endpoints)

  
### Docker Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/MasakDirt/spy-cat-agency.git
   cd spy-cat-agency
   ```
   
2. **Set Up Environment Variables**
   Create a `.env` file in the project root with the following:
   ```
    DJANGO_SECRET=<your_django_secret>
    DJANGO_DEBUG=<False>
    PRODUCTION=<False>
    
    POSTGRES_PASSWORD=<your_postgres_password>
    POSTGRES_USER=<your_postgres_user>
    POSTGRES_DB=<your_postgres_db>
    POSTGRES_HOST=<your_postgres_host>
    POSTGRES_PORT=<your_postgres_post>
    
    PGDATA=<your_postgres_pg_data>
    
    API_URL=https://api.thecatapi.com/v1/breeds
   ```
   
3. **Run docker-compose.yaml**
    ```bash
   docker-compose up --build
    ```

### Manual Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/MasakDirt/spy-cat-agency.git
   cd spy-cat-agency
   ```

2. **Set Up Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the project root with the following:
   ```
    DJANGO_SECRET=<your_django_secret>
    DJANGO_DEBUG=<False>
    PRODUCTION=<False>
    
    POSTGRES_PASSWORD=<your_postgres_password>
    POSTGRES_USER=<your_postgres_user>
    POSTGRES_DB=<your_postgres_db>
    POSTGRES_HOST=<your_postgres_host>
    POSTGRES_PORT=<your_postgres_post>
    
    PGDATA=<your_postgres_pg_data>
    
    API_URL=https://api.thecatapi.com/v1/breeds
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```


### Running Tests

Run the test suite to ensure the system works as expected:

```bash
python manage.py test
```

---

## API Endpoints

### Base URL

`http://127.0.0.1:8000/api/v1/agency/`

### Endpoints

| **Endpoint**                     | **Method**   | **Description**                  |
|----------------------------------|--------------|----------------------------------|
| `/spy_cats/`                     | `POST`       | Create a new spy cat             |
| `/spy_cats/`                     | `GET`        | List all spy cats                |
| `/spy_cats/<id>/`                | `GET`        | Retrieve a specific spy cat      |
| `/spy_cats/<id>/`                | `PATCH, PUT` | Update spy cat salary            |
| `/spy_cats/<id>/`                | `DELETE`     | Remove a spy cat                 |
| `/missions/`                     | `POST`       | Create a new mission             |
| `/missions/`                     | `GET`        | List all missions                |
| `/missions/<id>/`                | `GET`        | Retrieve a specific mission      |
| `/missions/<id>/assign_cat/`     | `POST`       | Assign cat to the mission        |
| `/missions/<id>/update_targets/` | `PATCH`      | Update mission targets           |
| `/missions/<id>/`                | `DELETE`     | Delete a mission (if unassigned) |

---

## Postman Collection

The Postman collection defining all endpoints is available [here](https://gold-escape-453583.postman.co/workspace/My-Workspace~522f2196-eeb6-4a10-8981-8409820e09a0/collection/26877648-d82a34ee-b370-4a8a-8486-4d898d60ce0a?action=share&creator=26877648&active-environment=26877648-ea9c11e7-dc3a-47a9-914d-b8e940fbac6b).

---

## Notes

- Missions and targets are created together to streamline the process.
- Validation ensures robust error handling and prevents data inconsistencies.
- Adheres to RESTful API best practices.
