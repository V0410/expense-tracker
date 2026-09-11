# Expense Tracker — CLI + REST API

A Python expense tracker that started as a command-line tool and grew into a Flask REST API backed by SQLite, with a pytest suite covering the API.

## Features

**CLI**
- Add, view, update, delete, and search expenses
- Monthly totals and category filtering
- Dates are recorded automatically
- Input validation, persistent SQLite storage

**REST API**
- Full CRUD on expenses (`GET`, `POST`, `PUT`, `DELETE`)
- Filter by category, minimum amount, or month — combine as needed
- JSON in, JSON out, with proper HTTP status codes
- Request validation and parameterized SQL queries

**Testing**
- pytest suite using Flask's test client
- Runs against an isolated temporary database, so tests never touch `expenses.db`
- Covers CRUD, validation, and all the filter combinations

## Tech stack

Python 3.10+, Flask, SQLite, pytest, Git/GitHub. Core modules: `sqlite3`, `datetime`, `flask`, `pytest`.

## Project structure

```text
expense-tracker/
│
├── app/
│   ├── __init__.py          # Flask application setup
│   ├── database.py          # SQLite connection and database helpers
│   ├── routes.py            # REST API routes
│   └── validation.py        # Expense validation rules
│
├── tests/
│   ├── conftest.py          # Test database and Flask test client setup
│   └── test_expenses.py     # API tests
│
├── main.py                  # Original CLI application
├── expenses.db              # SQLite database (generated locally)
├── requirements.txt         # Python dependencies
├── .gitignore
└── README.md
```

`expenses.db` is generated locally and excluded from Git.

## Requirements

Python 3.10+ and pip. The Flask API and test suite need the packages in `requirements.txt`.

## Installation

Clone the repo:

```bash
git clone https://github.com/V0410/expense-tracker.git
cd expense-tracker
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows: `.venv\Scripts\activate`
macOS/Linux: `source .venv/bin/activate`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the CLI

```bash
python main.py
```

The SQLite database is created automatically if it doesn't already exist.

## Running the Flask API

```bash
flask --app app run --debug
```

The API runs at `http://127.0.0.1:5000`.

## Running tests

```bash
python -m pytest
```

Tests run against a temporary SQLite database, so they won't touch your real `expenses.db`.

## CLI menu

```text
====================
   Expense Tracker
====================

1. Add Expense
2. View Expenses
3. Update Expense
4. Monthly Total
5. Delete Expense
6. Search Expense
7. Category Filter
8. Exit
```

## Expense data

| Field | Description |
|---|---|
| `id` | Automatically generated unique identifier |
| `name` | Name of the expense |
| `amount` | Expense amount |
| `category` | Expense category |
| `date` | Automatically recorded date, `YYYY-MM-DD` |

The CLI and REST API share the same SQLite database.

## REST API

Base URL: `http://127.0.0.1:5000`

### `GET /expenses`

Returns all expenses.

```json
[
  {
    "id": 1,
    "name": "burger",
    "amount": 140.0,
    "category": "food",
    "date": "2020-08-10"
  }
]
```

`200 OK`

### `GET /expenses/<id>`

Returns a single expense.

```json
{
  "id": 1,
  "name": "burger",
  "amount": 140.0,
  "category": "food",
  "date": "2020-08-10"
}
```

`200 OK`. If the id doesn't exist: `404 Not Found` with `{"error": "Expense not found"}`.

### `POST /expenses`

```http
POST /expenses
Content-Type: application/json
```

```json
{
  "name": "Coffee",
  "amount": 120.50,
  "category": "food"
}
```

`id` and `date` are generated server-side.

```json
{
  "message": "Expense created",
  "expense": {
    "id": 2,
    "name": "Coffee",
    "amount": 120.5,
    "category": "food",
    "date": "2026-09-11"
  }
}
```

`201 Created`

### `PUT /expenses/<id>`

```http
PUT /expenses/1
Content-Type: application/json
```

```json
{
  "name": "Dinner",
  "amount": 350.50,
  "category": "food"
}
```

`id` and `date` stay unchanged.

```json
{
  "message": "Expense updated successfully",
  "expense": {
    "id": 1,
    "name": "Dinner",
    "amount": 350.5,
    "category": "food",
    "date": "2020-08-10"
  }
}
```

`200 OK`

### `DELETE /expenses/<id>`

```json
{
  "message": "Expense deleted successfully"
}
```

`200 OK`. If the id doesn't exist: `404 Not Found` with `{"error": "Expense not found"}`.

## Filtering

`GET /expenses` takes optional query parameters, which can be combined.

**Category**
```http
GET /expenses?category=food
```
Allowed values: `food`, `transport`, `shopping`, `bills`, `other`.

**Minimum amount**
```http
GET /expenses?min_amount=100.50
```
Returns expenses with an amount ≥ 100.50.

**Month** (`YYYY-MM`)
```http
GET /expenses?month=2026-09
```

**Combined**
```http
GET /expenses?category=food&min_amount=100.50&month=2026-09
```

## Validation

- `name` — required string, can't be empty or whitespace-only
- `amount` — required number, must be finite and greater than zero
- `category` — required, must be one of `food`, `transport`, `shopping`, `bills`, `other`

Invalid input returns `400 Bad Request`.

## HTTP status codes

| Status | Meaning |
|---|---|
| `200` | Request completed successfully |
| `201` | Expense created |
| `400` | Invalid client input |
| `404` | Expense not found |
| `405` | Method not allowed for the route |

## Database

SQLite via Python's `sqlite3` module, with a single `expenses` table (`id`, `name`, `amount`, `category`, `date`). All user-provided values go through parameterized queries.

## Testing

pytest with Flask's test client, run against a temporary database so test runs never affect real data. Covers retrieval, creation, updates, deletion, missing resources, invalid input, and every filter combination.

```bash
python -m pytest
```

## What I learned

This started as a plain JSON-file CLI tool, then moved to SQLite once parsing files by hand got old. From there I wrapped the same database in a Flask API and added a pytest suite on top.

Along the way: writing and refactoring CLI logic in Python, exception handling and input validation, SQLite CRUD (`CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, `WHERE`, `LIKE`, `SUM`) with parameterized queries, Flask app structure and application factories, routing with dynamic URL and query parameters, JSON request/response handling, and testing an API with pytest fixtures and an isolated test database. Also picked up better Git habits along the way — branching, smaller commits, working feature by feature instead of one giant push.

## Project evolution

JSON files → SQLite-backed CLI → Flask REST API on the same database → pytest suite with its own isolated test database.

```text
                    Expense Tracker
                          │
               ┌──────────┴──────────┐
               │                     │
           CLI Interface         REST API
               │                     │
            main.py                Flask
               │                     │
               └──────────┬──────────┘
                          ↓
                       SQLite
                          │
                          ↓
                     pytest tests
```

## Future improvements

Authentication, pagination, sorting, better search, OpenAPI/Swagger docs, Docker, a move to PostgreSQL, and eventually cloud deployment with a proper WSGI server and CI/CD.

## Contributing

Built mainly for learning and as a portfolio piece, but suggestions are welcome.

## License

Educational use.

## Author

**Vansh Gokhale**
Aspiring Python Backend & Cloud Engineer