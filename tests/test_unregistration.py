from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_sign_up_participant_for_activity():
    # Arrange
    activity_name = "Soccer Team"
    email = "new-player@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    refreshed = client.get("/activities")
    assert email in refreshed.json()[activity_name]["participants"]


def test_duplicate_signup_returns_400():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    refreshed = client.get("/activities")
    assert email not in refreshed.json()[activity_name]["participants"]


def test_unregister_unknown_participant_returns_404():
    # Arrange
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in this activity"
