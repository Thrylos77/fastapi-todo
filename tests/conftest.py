from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.core import Base
from app.models.user import User
from app.models.todo import Todo
from app.auth.model import TokenData
from app.auth.service import get_hashed_password
from app.core.rate_limiting import limiter

import pytest
import warnings

@pytest.fixture(scope="function")
def db_session():
    # User a unique databse URL for testing
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_user(db_session):

    # Create a test user
    hashed_password = get_hashed_password("password@123")
    user = User(
        id=uuid4(),
        first_name="Test",
        last_name="User",
        username="conftest",
        email="conftest@example.com",
        hashed_password=hashed_password
    )
    return user

@pytest.fixture(scope="function")
def test_token_data():
    return TokenData(user_id=str(uuid4()))

@pytest.fixture(scope="function")
def test_todo(test_token_data):
    return Todo(
        id=uuid4(),
        title="Test Todo",
        description="This is a test todo item.",
        is_completed=False,
        created_at=datetime.now(timezone.utc),
        user_id=test_token_data.get_uuid()
    )

@pytest.fixture(scope="function")
def client(db_session):
    from app.main import app
    from app.db.core import get_db

    # Disable rate limitting for tests
    limiter.reset()

    def overrride_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = overrride_get_db

    from fastapi.testclient import TestClient
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def auth_headers(client, db_session):
    # Register a test user
    response = client.post(
        "/auth/register", 
        json={
            "first_name": "Test",
            "last_name": "USER",
            "username": "conftest",
            "email": "conftest@example.com",
            "password": "password@123"
        }
    )
    assert response.status_code == 201

    # Login to get access token
    response = client.post(
        "/auth/token",
        data={
            "username": "conftest",
            "password": "password@123",
            "grant_type": "password"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}