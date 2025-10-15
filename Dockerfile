FROM python:3.12-slim

WORKDIR /fastapi-todo

# Install Poetry
RUN pip install poetry

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Install dependencies
COPY pyproject.toml /fastapi-todo/

RUN poetry install --no-interaction --no-root

# Copy the project files
COPY app/ app/

# Expose the port FastAPI runs on
EXPOSE 9000

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]

