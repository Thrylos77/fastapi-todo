from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    username: str
    email: EmailStr

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    confirm_new_password: str