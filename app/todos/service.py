from uuid import UUID, uuid4
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.todo import Todo
from . import model
from app.auth.model import TokenData
from app.core.exceptions import TodoCreationError, TodoNotFoundError

import logging

def create_todo(current_user: TokenData, db: Session, todo: model.TodoCreate) -> Todo:
    try:
        new_todo = Todo(**todo.model_dump())
        new_todo.user_id = current_user.get_uuid()
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        logging.info(f"Todo created successfully: {new_todo.id}")
        return new_todo
    except Exception as e:
        logging.error(f"Error creating todo for user {current_user.get_uuid()}. Error: {str(e)}")
        raise TodoCreationError()

def get_todos(current_user: TokenData, db: Session) -> list[model.TodoResponse]:
    todos = db.query(Todo).filter(Todo.user_id == current_user.get_uuid()).all()
    logging.info(f"Retrieved {len(todos)} todos for user: {current_user.get_uuid()}")
    return todos

def get_todo_by_id(current_user: TokenData, db: Session, todo_id: UUID) -> Todo:
    todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.user_id == current_user.get_uuid()).first()
    if not todo:
        logging.warning(f"Todo not found: {todo_id} for user: {current_user.get_uuid()}")
        raise TodoNotFoundError()
    logging.info(f"Retrieved todo: {todo.id} for user: {current_user.get_uuid()}")
    return todo

def update_todo(current_user: TokenData, db: Session, todo_id: UUID, todo_update: model.TodoCreate) -> Todo:
    todo_data = todo_update.model_dump(exclude_unset=True)
    todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.user_id == current_user.get_uuid()).update(todo_data)
    db.commit()
    db.refresh(todo)
    if not todo:
        logging.warning(f"Todo not found for update: {todo_id} for user: {current_user.get_uuid()}")
        raise TodoNotFoundError()
    logging.info(f"Todo updated successfully: {todo.id} for user: {current_user.get_uuid()}")
    return get_todo_by_id(current_user, db, todo_id)

def complete_todo(current_user: TokenData, db: Session, todo_id: UUID) -> Todo:
    todo = get_todo_by_id(current_user, db, todo_id)
    if todo.is_completed:
        logging.debug(f"Todo {todo_id} already completed")
        return todo
    todo.is_completed = True
    todo.competed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(todo)
    logging.info(f"Todo {todo_id} marked as completed by user: {current_user.get_uuid()}")
    return todo

def delete_todo(current_user: TokenData, db: Session, todo_id: UUID) -> None:
    todo = get_todo_by_id(current_user, db, todo_id)
    if not todo:
        logging.warning(f"Todo not found for deletion: {todo_id} for user: {current_user.get_uuid()}")
        raise TodoNotFoundError()
    db.delete(todo)
    db.commit()
    logging.info(f"Todo {todo_id} deleted successfully for user: {current_user.get_uuid()}")