# Expense Tracker API

A backend REST API for managing personal expenses, built with **Python, Flask, SQLAlchemy, and SQLite**. The project includes CRUD operations, request validation, filtering, automated testing, and database migrations.

The project originally started as a command-line expense tracker and was progressively developed into a REST API to practice real-world backend development concepts.

## 🚀 Features

### REST API
- Create, read, update, and delete expenses
- Retrieve a single expense by ID
- JSON request and response handling
- Proper HTTP status codes
- Query parameter-based filtering

### Filtering
Expenses can be filtered by:
- Category
- Minimum amount
- Month
- Multiple filters at the same time

Example:

```http
GET /expenses?category=food&min_amount=100&month=2026-09
```

### Validation
- Validates request body structure
- Required field validation
- Data type validation
- Empty/whitespace input validation
- Expense amount validation
- Category validation
- Invalid requests return appropriate `400 Bad Request` responses

### Database
- SQLite database
- SQLAlchemy ORM
- Database migrations
- Persistent expense storage
- Database schema managed through migrations

### Authentication
- User registration
- User login
- Password hashing
- Input validation for authentication requests

### Testing
- Automated tests using `pytest`
- Flask test client
- Isolated test database
- Tests for CRUD operations
- Validation tests
- Authentication validation tests
- Query parameter and filtering tests

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | REST API framework |
| SQLAlchemy | ORM / database interaction |
| SQLite | Database |
| Alembic / Flask-Migrate | Database migrations |
| Pytest | Automated testing |
| Git | Version control |
| GitHub | Code hosting |

---

## 📂 Project Structure

```text
expense-tracker/
│
├── app/
│   ├── __init__.py          # Flask application setup
│   ├── database.py          # Database configuration/helpers
│   ├── routes.py            # API routes
│   └── validation.py        # Request validation
│
├── migrations/              # Database migration files
│
├── tests/
│   ├── conftest.py          # Test configuration and fixtures
│   └── test_expenses.py     # API tests
│
├── main.py                  # Original CLI application
├── requirements.txt         # Project dependencies
├── .gitignore
└── README.md
```

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/V0410/expense-tracker.git
cd expense-tracker
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the database

The project uses SQLite for local development.

Apply the database migrations:

```bash
flask --app app db upgrade
```

### 6. Run the API

```bash
flask --app app run --debug
```

The API will be available at:

```text
http://127.0.0.1:5000
```

---

# 📡 API Endpoints

## Get all expenses

```http
GET /expenses
```

Example response:

```json
[
    {
        "id": 1,
        "name": "Coffee",
        "amount": 120.5,
        "category": "food",
        "date": "2026-09-11"
    }
]
```

---

## Get a single expense

```http
GET /expenses/<id>
```

Example:

```http
GET /expenses/1
```

Returns:

```json
{
    "id": 1,
    "name": "Coffee",
    "amount": 120.5,
    "category": "food",
    "date": "2026-09-11"
}
```

Returns `404 Not Found` if the expense does not exist.

---

## Create an expense

```http
POST /expenses
```

Request:

```json
{
    "name": "Coffee",
    "amount": 120.50,
    "category": "food"
}
```

The server generates the ID and date.

Response:

```json
{
    "message": "Expense created",
    "expense": {
        "id": 1,
        "name": "Coffee",
        "amount": 120.5,
        "category": "food",
        "date": "2026-09-11"
    }
}
```

Status:

```text
201 Created
```

---

## Update an expense

```http
PUT /expenses/<id>
```

Request:

```json
{
    "name": "Dinner",
    "amount": 350.50,
    "category": "food"
}
```

The expense ID and original date remain unchanged.

---

## Delete an expense

```http
DELETE /expenses/<id>
```

Example:

```http
DELETE /expenses/1
```

Response:

```json
{
    "message": "Expense deleted successfully"
}
```

---

# 🔎 Filtering

The `GET /expenses` endpoint supports optional query parameters.

### Filter by category

```http
GET /expenses?category=food
```

Available categories:

```text
food
transport
shopping
bills
other
```

### Filter by minimum amount

```http
GET /expenses?min_amount=100
```

Returns expenses where:

```text
amount >= 100
```

### Filter by month

```http
GET /expenses?month=2026-09
```

### Combine filters

```http
GET /expenses?category=food&min_amount=100&month=2026-09
```

---

# 🔐 Authentication

The API includes basic user authentication functionality.

### Register

```http
POST /register
```

### Login

```http
POST /login
```

User input is validated before processing, and passwords are stored using password hashing rather than plain text.

---

# 🧪 Testing

Run the complete test suite with:

```bash
python -m pytest
```

The tests use an isolated database so that testing does not modify the application's development database.

The test suite covers areas including:

- Expense CRUD operations
- Request validation
- Invalid input handling
- Filtering
- User registration validation
- Login validation
- JSON payload validation

---

# 🗄️ Database Migrations

Database schema changes are managed through migrations.

This allows the database structure to evolve without manually recreating the database whenever the application's models change.

To apply existing migrations:

```bash
flask --app app db upgrade
```

---

# 📋 HTTP Status Codes

| Status Code | Meaning |
|---|---|
| `200 OK` | Request completed successfully |
| `201 Created` | Resource successfully created |
| `400 Bad Request` | Invalid client input |
| `404 Not Found` | Requested resource does not exist |
| `405 Method Not Allowed` | HTTP method is not supported for the route |

---

# 🎯 What I Practiced

This project was built progressively to practice backend development concepts including:

- Python backend development
- REST API design
- HTTP methods and status codes
- Flask routing
- Request and response handling
- Query parameters
- Input validation
- SQL and database interaction
- SQLAlchemy ORM
- Database migrations
- Password hashing
- Automated testing
- Test databases and fixtures
- Git and GitHub
- Project structure and backend organization

---

## 📌 Future Improvements

Potential future improvements include:

- JWT-based authentication
- Pagination
- Expense summaries and reporting endpoints
- PostgreSQL support
- API documentation with Swagger/OpenAPI
- Docker containerization
- CI/CD with GitHub Actions
- Cloud deployment

---

## 👨‍💻 Author

**Vansh Gokhale**

GitHub:  
https://github.com/V0410