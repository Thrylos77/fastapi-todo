from uuid import uuid4

from app.todos import service as todos_service
from app.todos.model import TodoCreate
from app.models.todo import Todo
from app.core.exceptions import TodoNotFoundError

import pytest

class TestTodoService:
    def test_create_todo(self, db_session, test_token_data):
        todo_create = TodoCreate(
            title="New Title",
            description="New Description"
        )

        new_todo = todos_service.create_todo(test_token_data, db_session, todo_create)
        assert new_todo.title == "New Title"
        assert new_todo.description == "New Description"
        assert new_todo.user_id == test_token_data.get_uuid()
        assert not new_todo.is_completed

    def test_get_todos(self, db_session, test_token_data, test_todo):
        test_todo.user_id = test_token_data.get_uuid()
        db_session.add(test_todo)
        db_session.commit()

        todos = todos_service.get_todos(test_token_data, db_session)
        assert len(todos) == 1
        assert todos[0].id == test_todo.id

    def test_get_todo_by_id(self, db_session, test_token_data, test_todo):
        test_todo.user_id = test_token_data.get_uuid()
        db_session.add(test_todo)
        db_session.commit()

        todo = todos_service.get_todo_by_id(test_token_data, db_session, test_todo.id)
        assert todo.id == test_todo.id

        with pytest.raises(TodoNotFoundError):
            todos_service.get_todo_by_id(test_token_data, db_session, uuid4())

    def test_complete_todo(self, db_session, test_token_data, test_todo):
        test_todo.user_id = test_token_data.get_uuid()
        db_session.add(test_todo)
        db_session.commit()

        complete_todo = todos_service.complete_todo(test_token_data, db_session, test_todo.id)
        assert complete_todo.is_completed
        # assert complete_todo.completed_at is not None

    def test_delete_todo(self, db_session, test_token_data, test_todo):
        test_todo.user_id = test_token_data.get_uuid()
        db_session.add(test_todo)
        db_session.commit()

        todos_service.delete_todo(test_token_data, db_session, test_todo.id)
        assert db_session.query(Todo).filter_by(id=test_todo.id).first() is None