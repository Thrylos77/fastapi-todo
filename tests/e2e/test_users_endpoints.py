from fastapi.testclient import TestClient

def test_get_current_user(client: TestClient, auth_headers):
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    user_data = response.json()
    assert "first_name" in user_data
    assert "last_name" in user_data
    assert "username" in user_data
    assert "email" in user_data
    assert "hashed_password" not in user_data


def test_change_password(client: TestClient, auth_headers):
    # Change password
    response = client.put(
        "/users/change-password",
        json={
            "current_password": "password@123",
            "new_password": "newpassword@123",
            "confirm_new_password": "newpassword@123"
        },
        headers=auth_headers
    )
    assert response.status_code == 200

    # Try Logging with new password
    login_response = client.post(
        "/auth/token",
        data={
            "username": "conftest",
            "password": "newpassword@123",
            "grant_type": "password"
        }
    )
    assert login_response.status_code == 200

def test_password_change_validation(client: TestClient, auth_headers):
    # Test wrong current password
    response = client.put(
        "/users/change-password",
        json={
            "current_password": "wrongpassword",
            "new_password": "newpassword@123",
            "confirm_new_password": "newpassword@123"
        },
        headers=auth_headers
    )
    assert response.status_code == 401

    # Test password mismatch
    response = client.put(
        "/users/change-password",
        json={
            "current_password": "password@123",
            "new_password": "newpassword@123",
            "confirm_new_password": "wrongpassword"
        },
        headers=auth_headers
    )

