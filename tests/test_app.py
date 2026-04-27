from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities_returns_success():
    response = client.get("/activities")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()


def test_signup_for_activity_success():
    email = "newstudent@mergington.edu"

    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]


def test_signup_for_same_activity_twice_fails():
    email = "duplicate@mergington.edu"

    first_response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": email},
    )
    second_response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": email},
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up"


def test_delete_signup_success():
    email = "remove-me@mergington.edu"

    client.post(
        "/activities/Gym%20Class/signup",
        params={"email": email},
    )

    response = client.delete(
        "/activities/Gym%20Class/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert "Removed" in response.json()["message"]