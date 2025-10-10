from fastapi import FastAPI
from .db.core import engine, Base
from .models.todo import Todo
from .models.user import User
from .api.v1.routes import register_routes

from .core.logging import configure_logging, LogLevels

configure_logging(LogLevels.INFO)

app = FastAPI()

"""
Only uncomment the line below if you want to create new tables automatically.
Otherwise, the tests will fail if not connected.
"""
# Base.metadata.create_all(bind=engine)

register_routes(app)