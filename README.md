# Expense Tracker API

A REST API for managing personal expenses. Built with FastAPI, SQLAlchemy, PostgreSQL, and JWT bearer authentication.

## Features

- Register users and authenticate with a JWT access token
- Create, read, update, and delete expenses scoped to the signed-in user
- Retrieve expense categories
- Validate request and response data with Pydantic
- Interactive API documentation through Swagger UI

## Tech stack

- Python 3
- FastAPI and Uvicorn
- SQLAlchemy
- PostgreSQL (`psycopg2`)
- Pydantic Settings
- `python-jose` for JWTs
- `pwdlib` for password hashing

## Getting started

### 1. Clone the project

```bash
git clone <repository-url>
cd ExpenseTrackerAPI
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DB_CONNECTION=postgresql://postgres:your-password@localhost:5432/expense_tracker
ACCESS_TOKEN_EXPIRE_MINUTES=60
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
```

Create the PostgreSQL database named in `DB_CONNECTION` before starting the application. Tables are created automatically when the app starts.

### 5. Run the API

```bash
uvicorn main:app --reload
```

The service will be available at `http://127.0.0.1:8000`.

## API documentation

Once the server is running, use:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Authentication flow

1. Create an account with `POST /users/create`.
2. Sign in with `POST /users/login` to receive an access token.
3. Send the token on protected expense requests:

```http
Authorization: Bearer <access_token>
```

In Swagger UI, click **Authorize** and enter `Bearer <access_token>`.

## Endpoints

### Users

| Method | Path | Authentication | Description |
| --- | --- | --- | --- |
| `POST` | `/users/create` | No | Create a user account |
| `POST` | `/users/login` | No | Sign in and receive a JWT |

Create user example:

```json
{
  "username": "alex",
  "email": "alex@example.com",
  "password": "strong-password"
}
```

Login example:

```json
{
  "username": "alex",
  "password": "strong-password"
}
```

### Categories

| Method | Path | Authentication | Description |
| --- | --- | --- | --- |
| `GET` | `/categories/get` | No | List all categories |
| `GET` | `/categories/get/{category_id}` | No | Get one category |

### Expenses

All expense endpoints require a bearer token. An expense is available only to the user who created it.

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/expenses/create` | Create an expense |
| `GET` | `/expenses/get` | List the current user's expenses |
| `GET` | `/expenses/get/{expense_id}` | Get one expense |
| `PUT` | `/expenses/update/{expense_id}` | Update an expense |
| `DELETE` | `/expenses/delete/{expense_id}` | Delete an expense |

Create or update expense body:

```json
{
  "title": "Lunch",
  "price": 12.5,
  "category_id": 1
}
```

## Categories setup

The currently exposed API only reads categories, so add at least one category directly to the database before creating an expense. For example:

```sql
INSERT INTO categories (name) VALUES
  ('Food'),
  ('Transport'),
  ('Utilities');
```

Use a `category_id` returned by `GET /categories/get` when creating or updating an expense.

## Project structure

```text
.
├── main.py                 # FastAPI application and router setup
├── models/                 # SQLAlchemy database models
├── routers/                # User, category, expense, and auth logic
├── schemas/                # Pydantic request/response schemas
├── utils/                  # Database, settings, and security utilities
├── requirements.txt
└── .env                    # Local configuration (not committed)
```

## Notes

- CORS is currently open to all origins for development convenience. Restrict `allow_origins` before deploying to production.
- Keep `.env` out of version control and use a unique, securely generated `SECRET_KEY` in production.
