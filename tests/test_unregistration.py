from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")

    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    refreshed = client.get("/activities")
    assert email not in refreshed.json()[activity_name]["participants"]


def test_unregister_unknown_participant_returns_404():
    response = client.post("/activities/Chess Club/unregister?email=missing@mergington.edu")

    assert response.status_code == 404
