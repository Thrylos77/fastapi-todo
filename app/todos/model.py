from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from ..models.todo import Priority
from datetime import datetime

class TodoBase(BaseModel):
    description: str
    due_date: Optional[datetime] = None
    priority: Priority = Priority.Normal

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: UUID
    is_completed: bool
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)