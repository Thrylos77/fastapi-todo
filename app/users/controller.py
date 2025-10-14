from fastapi import APIRouter, status
from uuid import UUID

from app.db.core import DbSession
from . import model, service
from app.auth.service import CurrentUser

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", response_model=model.UserResponse)
def get_current_user(current_user: CurrentUser, db: DbSession):
    return service.get_user_by_id(db, current_user.get_uuid())


@router.put("/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
        pwd_change: model.PasswordChange,
        db: DbSession,
        current_user: CurrentUser ):

    service.change_password(db, current_user.get_uuid(), pwd_change)