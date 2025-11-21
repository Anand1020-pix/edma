# Expense Budget Management API

A FastAPI-based service that lets you track users, their salaries, and categorized expenses with convenient aggregation endpoints for totals and breakdowns.

## Features

- Async PostgreSQL persistence powered by SQLAlchemy 2.0 and asyncpg
- REST endpoints for managing users and expenses
- Rich filtering for expense history (day, week, month, year, category)
- Budget summary endpoint delivering totals and category breakdowns
- Auto-generated OpenAPI docs via FastAPI (Swagger UI and ReDoc)

## Project Structure

```
app/
  db.py              # Database engine and session management
  main.py            # FastAPI application bootstrap
  model.py           # SQLAlchemy ORM models and enums
  schemas.py         # Pydantic request/response schemas
  users/             # User domain (router, service, repository)
  expenses/          # Expense domain (router, service, repository)
```

## Requirements

- Python 3.11+
- PostgreSQL database
- Access to install dependencies from `pip`

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Anand1020-pix/edma.git
   cd edma
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Linux/macOS
   .venv\Scripts\activate       # Windows PowerShell
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env` and update the values, or edit `.env` directly.
   - The key variable is `DB_URL`, for example:
     ```env
     DB_URL=postgresql+asyncpg://postgres:password@localhost:5432/EBMA
     ```
   - Ensure the target database (`EBMA` above) already exists in PostgreSQL.

5. **Apply database migrations / sync schema**
   - On startup the app will synchronize the schema defined in `model.py`.

## Running the API

```bash
uvicorn app.main:app --reload
```

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Overview

### Users

- `POST /users`
  - Body: `{ "username": "alice", "salary": 4500.0 }`
  - Response: created user with `user_id`, `username`, `salary`
  - Returns `400` if the username already exists.

### Expenses

- `POST /expenses`
  - Body: `{ "user_id": 1, "name": "Groceries", "amount": 120.5, "category": "Food" }`
  - Response: expense with `expense_id`, `created_at`, and category enum value
  - Returns `404` if the user does not exist
  - Returns `400` for invalid data (e.g., negative amount)

- `GET /expenses/{user_id}`
  - Query filters (optional): `day`, `week`, `month`, `year`, `category`
  - Response: list of expenses for the user filtered by supplied criteria

- `GET /expenses/totals/{user_id}`
  - Response:
    ```json
    {
      "total_expense": 2750.0,
      "total_salary": 5000.0,
      "remaining_amount": 2250.0,
      "category_breakdown": {
        "Food": 950.0,
        "Utilities": 600.0
      }
    }
    ```

## Testing Suggestions

- Use HTTP clients such as `curl`, HTTPie, or Thunder Client
- For exploratory testing, the Swagger UI supports live requests
- Consider adding automated tests with `pytest` and `httpx` for integration coverage

## Troubleshooting

- **IntegrityError on creating a user**: ensure the username is unique.
- **Foreign key violation on expenses**: verify the `user_id` exists before posting an expense.
- **asyncpg driver errors**: confirm the `DB_URL` scheme uses `postgresql+asyncpg` and that `asyncpg` is installed.



Happy budgeting!
