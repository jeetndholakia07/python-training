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
 app/
 ├── api/
  ├── v1/
   ├── endpoints/
 ├── core/
 ├── models/
 ├── repositories/
 ├── schemas/
 └── services/
 └── utils/
├── migrations/
├── _init_.py
├── .env
├── alembic.ini
├── main.py
├── README.md
├── requirements.txt

## Setup Instructions
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
DATABASE_URL=mysql:mysqlconnector://user:password@localhost/db
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