from fastapi.testclient import TestClient
from uuid import uuid4

def test_todo_crud_operation(client: TestClient, auth_headers):
    # Create a new todo
    create_response = client.post(
        "/todos/",
        json={
            "title": "Test Todo",
            "description": "This is a test todo item."
        },
        headers=auth_headers
    )
    assert create_response.status_code == 201
    todo_data = create_response.json()
    todo_id = todo_data["id"]
    assert todo_data["title"] == "Test Todo"
    assert todo_data["description"] == "This is a test todo item."
    assert not todo_data["is_completed"]

    # Get all todos
    list_response = client.get("/todos/", headers=auth_headers)
    assert list_response.status_code == 200
    todos = list_response.json()
    assert len(todos) > 0
    assert any(todo["id"] == todo_id for todo in todos)

    # Get a specific todo
    get_response = client.get(f"/todos/{todo_id}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json()["id"] == todo_id

    # Updata todo
    update_response = client.put(
        f"/todos/{todo_id}",
        json={
            "title": "Updated Todo",
            "description": "This is an updated todo item."
        },
        headers=auth_headers
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Todo"
    assert update_response.json()["description"] == "This is an updated todo item."

    # Complete todo
    complete_response = client.put(f"/todos/{todo_id}/complete", headers=auth_headers)
    assert complete_response.status_code == 200
    assert complete_response.json()["is_completed"]

    # Delete todo
    delete_response = client.delete(f"/todos/{todo_id}", headers=auth_headers)
    assert delete_response.status_code == 204