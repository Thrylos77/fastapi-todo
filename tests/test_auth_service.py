from datetime import timedelta
from uuid import uuid4
from fastapi.security import OAuth2PasswordRequestForm

from app.core.exceptions import AuthenticationError
from app.models.user import User
from app.auth import service as auth_service
from app.auth.model import RegisterUserRequest

import pytest

class TestAuthService:
    def test_verify_password(self):
        password = "password@123"
        hashed = auth_service.get_hashed_password(password)
        assert auth_service.verify_password(password, hashed)
        assert not auth_service.verify_password("wrongpassword", hashed)
    
    def test_user(self, db_session, test_user):
        db_session.add(test_user)
        db_session.commit()

        user = auth_service.authenticate_user(db_session, "testuser", "password@123")
        assert user is not False
        assert user.email == test_user.email or user.username == test_user.username
    
    def test_login_for_access_token(self, db_session, test_user):
        db_session.add(test_user)
        db_session.commit()

        class FormData:
            def __init__(self):
                self.username = "test@example.com"
                self.password = "password@123"
                self.scope = ""
                self.client_id = None
                self.client_secret = None

        form_data = FormData()
        token = auth_service.login_for_access_token(db_session, form_data)
        assert token.token_type == "bearer"
        assert token.access_token is not None

@pytest.mark.asyncio
async def test_register_user(db_session):
    request = RegisterUserRequest(
        first_name="New",
        last_name="USER",
        username="new",
        email="new@example.com",
        password="password@123"
    )
    auth_service.register_user(db_session, request)

    user = db_session.query(User).filter_by(email="new@example.com").first()
    assert user is not None
    assert user.email == "new@example.com"
    assert user.first_name == "New"
    assert user.last_name == "USER"
    assert user.username == "new"

def test_create_and_verify_token(db_session):
    user_id = uuid4()
    token = auth_service.create_access_token("test@example.com", "testuser", user_id, timedelta(minutes=30))

    token_data = auth_service.verify_token(token)
    assert token_data.get_uuid() == user_id

    # Test invalid credentials
    assert auth_service.authenticate_user(db_session, "test@example.com", "wrongpassword") is False

    with pytest.raises(AuthenticationError):
        form_data = OAuth2PasswordRequestForm(
            username="testuser",
            password="wrongpassword",
            scope="",
        )
        auth_service.login_for_access_token(db_session, form_data)