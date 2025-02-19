# 🚀 FastAPI Fitness Tracker

This is a simple FastAPI Fitness Tracker project.

## 📌 Features
- FastAPI for building APIs
- SQLAlchemy ORM for database interactions
- SQLite as the database
- Poetry for dependency management
- Pydantic for data validation
- Alembic for database migrations

---

## 🛠️ **Setup & Installation**

### **1️⃣ Clone the repository**
```sh
git clone https://github.com/sajith024/fastapi_fitness_tracker.git
cd fastapi_fitness_tracker
```

### **2️⃣ Install Poetry (if not installed)**
```sh
curl -sSL https://install.python-poetry.org | python3 -
```
or follow [Poetry installation guide](https://python-poetry.org/docs/#installing-with-the-official-installer).

### **3️⃣ Install dependencies**
```sh
poetry install
```

---

## ⚙️ **Project Structure**
```
fastapi_fitness_tracker/
│── alembic/            # Alembic migrations
│── app/
│   ├── models/         # SQLAlchemy database models
│   ├── core/           # Database connection & session
│   ├── schemas/        # Pydantic models
│   ├── crud/           # CRUD operations
│   ├── api/            # API routes
│   ├── main.py         # FastAPI application
│   │── dependencies.py
│   │── exception_handler.py
│   │── tasks.py
│── alembic.ini
│── .env                # Environment variables
│── pyproject.toml      # Poetry configuration
│── poetry.lock
│── README.md           # Documentation
```

---

## 🚀 **Running the API**
Run the FastAPI server using **Poetry**:
```sh
poetry run fastapi dev
```
The API will be available at: [click here](http://127.0.0.1:8000)  
📍 `http://127.0.0.1:8000`

The API Docs will be available at: [click here](http://127.0.0.1:8000/docs)  
📍 `http://127.0.0.1:8000/docs` (Swagger UI)

---

## 🔄 **Database Migrations with Alembic**
If using **Alembic** for migrations:

1. Generate a migration script:
   ```sh
   poetry run alembic revision --autogenerate -m "Initial migration"
   ```
2. Apply migrations:
   ```sh
   poetry run alembic upgrade head
   ```

---
