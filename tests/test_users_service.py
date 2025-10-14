from uuid import uuid4

from app.users import service as users_service
from app.users.model import PasswordChange
from app.auth import service as auth_service
from app.models.user import User
from app.core.exceptions import UserNotFoundError, InvalidPasswordError, PasswordMismatchError

import pytest

def test_get_user_by_id(db_session, test_user):
    db_session.add(test_user)
    db_session.commit()

    user = users_service.get_user_by_id(db_session, test_user.id)
    assert user.id == test_user.id
    assert user.email == test_user.email

    with pytest.raises(UserNotFoundError):
        users_service.get_user_by_id(db_session, uuid4())

def test_change_password(db_session, test_user):
    # Add the user to the database
    db_session.add(test_user)
    db_session.commit()

    # Test sucessful password change
    password_change = PasswordChange(
        current_password="password@123", # This matches the password set in test_user fixture
        new_password="newpassword@123",
        confirm_new_password="newpassword@123"
    )

    users_service.change_password(db_session, test_user.id, password_change)

    # Verify new password works
    updated_user = db_session.query(User).filter_by(id=test_user.id).first()
    assert auth_service.verify_password("newpassword@123", updated_user.hashed_password)

def test_change_password_invalid_current(db_session, test_user):
    db_session.add(test_user)
    db_session.commit()

    # Test invalid current password
    with pytest.raises(InvalidPasswordError):
        password_change = PasswordChange(
            current_password="wrongpassword",
            new_password="newpassword@123",
            confirm_new_password="newpassword@123"
        )
        users_service.change_password(db_session, test_user.id, password_change)
    
def test_change_password_mismatch(db_session, test_user):
    db_session.add(test_user)
    db_session.commit()

    # Test password miswmatch
    with pytest.raises(PasswordMismatchError):
        password_change = PasswordChange(
            current_password="password@123",
            new_password="newpassword@123",
            confirm_new_password="newpassword@"
        )
        users_service.change_password(db_session, test_user.id, password_change)