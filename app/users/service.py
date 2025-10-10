from uuid import UUID, uuid4
from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.user import User
from . import model
from ..core.exceptions import UserNotFoundError, InvalidPasswordError, PasswordMismatchError
from ..auth.service import verify_password, get_hashed_password

import logging

def get_user_by_id(db: Session, user_id: UUID) -> model.UserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logging.warning(f"User not found with ID: {user_id}")
        raise UserNotFoundError(user_id)
    logging.info(f"Successfully retrieved user with ID: {user_id}")
    return user

def change_password(db: Session, user_id: UUID, pwd_change: model.PasswordChange) -> None:
    try:
        user = get_user_by_id(db, user_id)

        # Verify current password
        if not verify_password(pwd_change.current_password, user.hashed_password):
            logging.warning(f"Invalid current password for user ID: {user_id}")
            raise InvalidPasswordError()
        
        # Check if new password and confirm password match
        if pwd_change.new_password != pwd_change.confirm_new_password:
            logging.warning(f"New password and confirm password do not match for user ID: {user_id}")
            raise PasswordMismatchError()
        
        # Update password
        user.hashed_password = get_hashed_password(pwd_change.new_password)
        db.commit()
        logging.info(f"Password changed successfully for user ID: {user_id}")
        return True
    except HTTPException as e:
        logging.error(f"Error changing password for user ID: {user_id}. Error: {str(e)}")
        raise e