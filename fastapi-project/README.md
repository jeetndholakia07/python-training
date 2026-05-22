# FastAPI Project

# Overview
This is a small demo project developed using FastAPI. The project is a sample backend application having CRUD operations for two entities - Company and Employee. It has APIs for Create, Read, Update and Soft Delete for both company and employee, with user authentication using JWT and role-based authorization. It also has global exception handlers, and is designed with modern architecture.

## Tech Stack
The tech stack for the project is as follows:
1) Python FastAPI
2) SQLAlchemy ORM
3) Pydantic
4) Alembic for Migrations
5) MySQL DB

## Project Structure

fastapi-project/

 &nbsp; app/

 &ensp;├── api/

 &emsp; ├── v1/

 &nbsp; &ensp; ├── endpoints/

 &ensp;├── core/

 &ensp;├── models/

 &ensp;├── repositories/

 &ensp;├── schemas/

 &ensp;└── services/

 &ensp;└── utils/

├── migrations/

├── _init_.py

├── .env

├── alembic.ini

├── main.py

├── pyproject.toml

├── README.md

├── requirements.txt

├── uv.lock

If you are using pip and venv then follow the setup instructions for pip and venv.
And if you are using package managers like uv then follow the setup instructions for uv.

## Setup Instructions for *pip and venv*
### 1. Clone the repo
```bash
git clone https://github.com/jeetndholakia07/python-training
cd fastapi-project
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env file
DATABASE_URL=mysql+mysqlconnector://user:password@localhost/db
JWT_SECRET=your_secret_key
JWT_ALGORITHM="HS256"
TOKEN_EXPIRY_MINUTES=any_token_expiry

### 5. Setup MySQL Database and Migrations
Run the following command for applying database migrations.
```bash
alembic upgrade head
```

### 6. Running the app
Development
```bash
uvicorn main:app --reload
```
Open the app on Swagger UI: http://localhost:8000/docs

### 7. API Documentation
Swagger UI: http://localhost:8000/docs

## Setup Instructions for *uv package manager*
### 1. Clone the repo
```bash
git clone https://github.com/jeetndholakia07/python-training
cd fastapi-project
```
### 2. Create virtual environment
```bash
uv add ruff
```

### 3. Install dependencies
```bash
uv sync
```

### 4. Create .env file
DATABASE_URL=mysql+mysqlconnector://user:password@localhost/db
JWT_SECRET=your_secret_key
JWT_ALGORITHM="HS256"
TOKEN_EXPIRY_MINUTES=any_token_expiry

### 5. Setup MySQL Database and Migrations
Run the following command for applying database migrations.
```bash
uv run alembic upgrade head
```

### 6. Running the app
Development
```bash
uv run uvicorn main:app --reload
```
Open the app on Swagger UI: http://localhost:8000/docs

## Testing
The app has unit tests for the service layer, and integration tests for the repository and 
controller or api layer using pytest and httpx asyncio.

To run the tests, use the following command after activating the virtual environment:

```bash
pytest
```