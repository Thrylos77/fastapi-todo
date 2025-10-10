from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

import uuid
from ..db.core import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __str__(self):
        return f"<User(email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}', username='{self.username}')>"