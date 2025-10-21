# FastAPI To-Do List Application

A simple yet powerful To-Do List application built with FastAPI, following best practices for project structure and modern Python development.

## Features

*   **User Authentication:** Secure user registration and login using JWT.
*   **To-Do Management:** Create, retrieve, update, and delete to-do items.
*   **User Management:** Basic user profile management.
*   **Database Integration:** Uses SQLAlchemy for ORM and Alembic for database migrations.
*   **Rate Limiting:** Protects against brute-force attacks.
*   **Asynchronous:** Built with `async` and `await` for high performance.
*   **Dependency Management:** Uses Poetry for managing project dependencies.

## Technologies Used

*   **Backend:**
    *   [Python 3.12+](https://www.python.org/)
    *   [FastAPI](https://fastapi.tiangolo.com/)
    *   [Uvicorn](https://www.uvicorn.org/)
    *   [SQLAlchemy](https://www.sqlalchemy.org/)
    *   [Alembic](https://alembic.sqlalchemy.org/en/latest/)
    *   [PostgreSQL](https://www.postgresql.org/) (with `psycopg2-binary`)
    *   [Pydantic](https://pydantic-docs.helpmanual.io/) (used by FastAPI)
    *   [SlowAPI](https://github.com/laurents/slowapi) for rate limiting
    *   [python-dotenv](https://github.com/theskumar/python-dotenv) for environment variables
    *   [Passlib](https://passlib.readthedocs.io/en/stable/) with `bcrypt` for password hashing
    *   [PyJWT](https://pyjwt.readthedocs.io/en/stable/) for JSON Web Tokens

*   **Development & Testing:**
    *   [Poetry](https://python-poetry.org/)
    *   [Pytest](https://docs.pytest.org/en/latest/)
    *   [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)
    *   [HTTPX](https://www.python-httpx.org/)
    *   [Black](https://github.com/psf/black)
    *   [Ruff](https://github.com/astral-sh/ruff)
    *   [MyPy](http://mypy-lang.org/)

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd fastapi-todo
    ```

2.  **Create a `.env` file:**
    Create a `.env` file in the root directory by copying the `.env.example` file. This file will contain your environment variables.
    ```bash
    cp .env.example .env
    ```
    Update the `.env` file with your database credentials and a secret key.

3.  **Install dependencies:**
    Make sure you have [Poetry](https://python-poetry.org/docs/#installation) installed. Then run:
    ```bash
    poetry install
    ```

4.  **Run database migrations:**
    ```bash
    poetry run alembic upgrade head
    ```

## Running the Application

To run the development server:
```bash
uvicorn app.main:app --reload
```
The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

The API is versioned under `/v1`.

*   **Auth:**
    *   `POST /auth/register`: Register a new user.
    *   `POST /auth/login`: Log in and receive a JWT token.

*   **Users:**
    *   `GET /users/me`: Get the current user's profile.
    *   `PUT /users/me`: Update the current user's profile.

*   **To-Dos:**
    *   `POST /todos/`: Create a new to-do item.
    *   `GET /todos/`: Get all to-do items for the current user.
    *   `GET /todos/{todo_id}`: Get a specific to-do item.
    *   `PUT /todos/{todo_id}`: Update a to-do item.
    *   `DELETE /todos/{todo_id}`: Delete a to-do item.

## Project Structure

```
├── app/
│   ├── api/            # API routers
│   ├── auth/           # Authentication logic
│   ├── core/           # Core components (logging, exceptions)
│   ├── db/             # Database session and core
│   ├── models/         # SQLAlchemy models
│   ├── todos/          # To-do specific logic
│   ├── users/          # User specific logic
│   └── main.py         # Main FastAPI application
├── tests/              # Unit tests
├── .env.example        # Example environment variables
├── docker-compose.yml
├── Dockerfile
├── poetry.lock
├── pyproject.toml      # Project dependencies
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature`).
6.  Open a pull request.
