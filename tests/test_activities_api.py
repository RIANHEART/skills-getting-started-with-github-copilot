from urllib.parse import quote
from src.app import activities


def test_get_activities(client):
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert "Chess Club" in data


def test_signup_success(client):
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    path = f"/activities/{quote(activity)}/signup"
    # ensure not already signed up
    assert email not in activities[activity]["participants"]
    r = client.post(path, params={"email": email})
    assert r.status_code == 200
    assert email in activities[activity]["participants"]
    assert "Signed up" in r.json()["message"]


def test_signup_duplicate(client):
    email = "duplicate@mergington.edu"
    activity = "Programming Class"
    path = f"/activities/{quote(activity)}/signup"
    # first signup succeeds
    r1 = client.post(path, params={"email": email})
    assert r1.status_code == 200
    # second signup should return 400
    r2 = client.post(path, params={"email": email})
    assert r2.status_code == 400


def test_signup_unknown_activity(client):
    email = "nobody@mergington.edu"
    path = "/activities/NoSuchActivity/signup"
    r = client.post(path, params={"email": email})
    assert r.status_code == 404


def test_delete_participant_success(client):
    activity = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{quote(activity)}/participants"
    # ensure participant exists
    assert email in activities[activity]["participants"]
    r = client.delete(path, params={"email": email})
    assert r.status_code == 200
    assert email not in activities[activity]["participants"]


def test_delete_participant_missing(client):
    activity = "Chess Club"
    email = "doesnotexist@mergington.edu"
    path = f"/activities/{quote(activity)}/participants"
    r = client.delete(path, params={"email": email})
    assert r.status_code == 404


def test_root_redirects_to_static(client):
    r = client.get("/", follow_redirects=False)
    assert r.status_code in (302, 307)
    assert r.headers.get("location") == "/static/index.html"
