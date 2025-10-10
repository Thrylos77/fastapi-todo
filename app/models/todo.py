from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime, timezone
from ..db.core import Base

import uuid
import enum

class Priority(enum.Enum):
    Low = 0
    Medium = 1
    Normal = 2
    High = 3
    Top = 4

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
    priority = Column(Enum(Priority), default=Priority.Normal)

    def __str__(self):
        return f"<Todo(description='{self.description}', due_date='{self.due_date}', is_completed='{self.is_completed}', priority='{self.priority}')>"
    