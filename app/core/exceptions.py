from fastapi import HTTPException

class TodoError(HTTPException):
    """Base exception for todo-related errors."""
    pass

class TodoNotFoundError(TodoError):
    def __init__(self, todo_id=None):
        if todo_id:
            message = f"Todo with id {todo_id} not found."
        else:
            message = "Todo not found."
        super().__init__(status_code=404, detail=message)
    
class TodoCreationError(TodoError):
    def __init__(self, error:str):
        super().__init__(status_code=500, detail=f"Failed to create todo: {error}")

class UserError(HTTPException):
    """Base exception for user-related errors."""
    pass

class UserNotFoundError(UserError):
    def __init__(self, user_id=None):
        if user_id:
            message = f"User with id {user_id} not found."
        else:
            message = "User not found."
        super().__init__(status_code=404, detail=message)

class PasswordMismatchError(UserError):
    def __init__(self):
        super().__init__(status_code=400, detail="Password does not match.")

class InvalidPasswordError(UserError):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid password.")

class AuthenticationError(HTTPException):
    def __init__(self, message: str = "Authentication failed."):
        super().__init__(status_code=401, detail=message)