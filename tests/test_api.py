from fastapi.testclient import TestClient

from src.main import create_app


client = TestClient(create_app())


def test_get_activities_returns_all_activities():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_get_participants_returns_activity_participants():
    response = client.get("/activities/Chess Club/participants")

    assert response.status_code == 200
    data = response.json()
    assert data["activity"] == "Chess Club"
    assert isinstance(data["participants"], list)


def test_get_participants_returns_404_for_unknown_activity():
    response = client.get("/activities/Unknown Club/participants")

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found, sorry"}


def test_signup_normalizes_email_and_signs_up():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "  NewStudent@Merginton.edu  "},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up newstudent@merginton.edu for Chess Club"
    }

    participants_response = client.get("/activities/Chess Club/participants")
    participants = participants_response.json()["participants"]
    assert "newstudent@merginton.edu" in participants


def test_signup_rejects_invalid_email_domain():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "student@example.com"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Email must use the @merginton.edu domain"
    }


def test_signup_rejects_duplicate_email():
    email = "repeatstudent@merginton.edu"
    first = client.post("/activities/Chess Club/signup", params={"email": email})
    second = client.post("/activities/Chess Club/signup", params={"email": email})

    assert first.status_code == 200
    assert second.status_code == 400
    assert second.json() == {"detail": "Student already signed up for this activity"}
