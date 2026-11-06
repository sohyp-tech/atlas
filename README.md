# Atlas — Book Sharing API

Atlas is an early-stage REST API project for sharing books and writing reviews. It is being built with Python and FastAPI, with SQLAlchemy for database access and MariaDB/MySQL as the intended database.

> **Status:** Work in progress. Some planned book and review routes are not implemented yet, and the current user routes still need fixes before the API is ready to run reliably. This repository is a learning project, not a production-ready service.

## Stack

- **Python** — application language
- **FastAPI** — HTTP API and interactive OpenAPI docs
- **Pydantic** — request-data validation
- **SQLAlchemy** — ORM/database access
- **MariaDB/MySQL** — relational database (`PyMySQL` driver)
- **Passlib** — password hashing utilities
- **python-dotenv** — local environment-variable loading

## Project layout

```text
atlas/
├── backend/
│   ├── main.py             # FastAPI app and router registration
│   ├── database/
│   │   ├── database.py     # Database engines and session dependencies
│   │   ├── models.py       # SQLAlchemy models
│   │   └── schema.py       # Pydantic request schemas
│   └── routers/
│       ├── users.py
│       ├── books.py
│       └── reverses.py
├── .env.example
└── requirements.txt
```

## Getting started

You need Python and a running MariaDB/MySQL server. The current database configuration expects separate database names for users, books, and reviews.

1. Clone the repository and enter it:

   ```bash
   git clone https://github.com/sohyp-tech/atlas.git
   cd atlas
   ```

2. Create and activate a virtual environment, then install dependencies:

   ```bash
   python -m venv .venv
   # Linux/macOS
   source .venv/bin/activate
   # Windows PowerShell: .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and set your MariaDB/MySQL credentials and database names. Create those databases on your server before starting the API.

4. Start the development server from the repository root:

   ```bash
   uvicorn main:app --app-dir backend --reload
   ```

   FastAPI's interactive documentation is normally available at `http://127.0.0.1:8000/docs` when the application starts successfully.

## Current limitations

- The book and review router files are currently empty.
- User routes and database setup need additional implementation and testing; the startup command above describes the intended development setup, but the current code may require fixes before it runs.
- Authentication, authorization, migrations, tests, and production deployment configuration are not complete.

## Contributing

Issues and pull requests are welcome. Please keep credentials out of commits: use a local `.env` file and never publish real database passwords.

## Author

Made with care by [Sohyp Khaled](https://github.com/sohyp-tech).
