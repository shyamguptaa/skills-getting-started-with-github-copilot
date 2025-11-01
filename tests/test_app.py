from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # basic sanity check for a known activity from sample data
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "test.student@mergington.edu"

    # Ensure clean starting state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Signing up again should fail with 400
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400

    # Unregister
    resp_un = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp_un.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregistering again should return 400
    resp_un2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp_un2.status_code == 400
